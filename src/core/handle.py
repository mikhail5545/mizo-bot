import sqlite3
import random
from aiogram import Dispatcher, html, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from datetime import datetime
import pytz

from core.messages import(command_start_message, command_calculate_message, command_address_message, command_order_admin_message,
                          command_url_message, command_last_message, command_confirm_message, command_confirm_order_admin_message,
                          command_confirm_admin_message, command_order_confirmed_message, command_cancel_admin_message, 
                          command_payment_confirmed_admin, command_payment_confirmed_user, command_cancel_confirmed_message, 
                          command_payment_declined_admin, command_payment_declined_user, command_active_order_user_message, command_order_shipped_admin, command_order_shipped_user)
from core.keyboard import(create_keyboard, create_sizes_keyboard, create_keyboard_admin, create_active_orders_keyboard, 
                          create_admin_events, create_user_orders_keyboard, create_user_events, create_canceled_orders_keyboard, create_colors_keyboard, UserCallback, AdminCallback)
from core.side import calculate, calculate_parsed
from core.classes import FlagStorage, Order, category_dict, Admin
from core.parse import parse_data

dp = Dispatcher()

async def handle_events(bot : Bot) -> None:
    """
    Main event handler.
    """

    con = sqlite3.connect('core/database/orders.db')
    flags = FlagStorage()
    order = Order()

    admin = Admin()

    # User callbacks
    @dp.message(CommandStart())
    async def command_start_handler(message : Message) -> None:
        admin.id = message.from_user.id
        await message.answer(
                text=await command_start_message(username=message.from_user.full_name), 
                parse_mode=ParseMode.HTML, 
                reply_markup=create_keyboard(['calculate', 'create_order', 'faq', 'ask'])
            )
    
    @dp.callback_query(UserCallback.filter(F.foo == 'delivery_type'))
    async def user_command_delivery_type(query: CallbackQuery, callback_data: UserCallback) -> None:
        await bot.send_message(
                chat_id=query.from_user.id, 
                text="Выберите тип доставки.", 
                reply_markup=create_keyboard(['fast_delivery', 'common_delivery'])
            )

    @dp.callback_query(UserCallback.filter((F.foo == 'fast_delivery') | (F.foo == 'common_delivery')))
    async def user_command_calculate_handler(query : CallbackQuery, callback_data : UserCallback) -> None:
        prev = flags.get(-1)
        if prev[0] + prev[1] == '!o':
            if callback_data.foo == 'fast_delivery':
                order.delivery_type = 'Быстрая доставка'
            else:
                order.delivery_type = 'Обычная доставка'
            await bot.send_message(
                chat_id=query.from_user.id, 
                text=f'Вы выбрали {'быструю' if order.delivery_type[0] == 'Б' else 'обычную'} доставку.', 
                parse_mode=ParseMode.HTML,
                reply_markup=create_keyboard(['url', 'back'])
            )
        else:    
            text = await command_calculate_message()
            flags.push(f'!{callback_data.foo[0]}!c')
            await bot.send_message(
                    chat_id=query.from_user.id, 
                    text=text, 
                    parse_mode=ParseMode.HTML
                )
    
    @dp.callback_query(UserCallback.filter(F.foo == 'back'))
    async def user_command_back_handler(query: CallbackQuery, callback_data: UserCallback) -> None:
        await bot.send_message(
                chat_id=query.from_user.id,
                text=await command_start_message(username=query.from_user.full_name), 
                parse_mode=ParseMode.HTML, 
                reply_markup=create_keyboard(['calculate', 'create_order', 'faq', 'ask', 'my_orders'])
            )
        
    @dp.callback_query(UserCallback.filter(F.foo == 'create_order'))
    async def user_command_create_order_handler(query: CallbackQuery, callback_data: UserCallback) -> None:
        order.user = query.from_user.id
        await bot.send_message(
                chat_id=query.from_user.id,
                text='Выберите категорию товара:',
                reply_markup=create_keyboard(['category', 'back'])
            )
        
    @dp.callback_query(UserCallback.filter(F.foo.contains('category_')))
    async def user_command_category_handler(query: CallbackQuery, callback_data: UserCallback) -> None:
        order.category = category_dict[callback_data.foo]
        flags.push("!o!d")
        await bot.send_message(
                chat_id=query.from_user.id,
                text="Выберите тип доставки.", 
                reply_markup=create_keyboard(['fast_delivery', 'common_delivery'])
            )
    
    @dp.callback_query(UserCallback.filter(F.foo == 'address'))
    async def user_command_address_handler(query: CallbackQuery, callback_data: UserCallback) -> None:
        text = await command_address_message()
        flags.push('!o!a')
        await bot.send_message(
                chat_id=query.from_user.id,
                text=text
            )

    @dp.callback_query(UserCallback.filter(F.foo == 'url'))
    async def user_command_url_handler(query: CallbackQuery, callback_data: UserCallback) -> None:
        text = await command_url_message()
        flags.push("!o!u")
        await bot.send_message(
                chat_id=query.from_user.id,
                text=text
            )
    
    @dp.callback_query(UserCallback.filter(F.foo == 'size'))
    async def user_command_size_handler(query: CallbackQuery, callback_data: UserCallback) -> None:
        label, price, style, colors = await parse_data(url=order.url)
        await bot.send_message(
                chat_id=query.from_user.id,
                text="Выберите размер: ",
                reply_markup=create_sizes_keyboard(price)
            )
    
    @dp.callback_query(UserCallback.filter(F.foo.contains('size_')))
    async def user_command_sizes_handler(query: CallbackQuery, callback_data: UserCallback) -> None:
        size = callback_data.foo.split("_")[1]
        label, price, style = await parse_data(url=order.url)
        order.label = label
        order.style = style
        order.size = size
        order.price = price[size]
        await bot.send_message(
                chat_id=query.from_user.id,
                text=f"Вы выбрали размер: {size}",
                reply_markup=create_keyboard(['last_step', 'back'])
            )

    @dp.callback_query(UserCallback.filter(F.foo == 'color'))
    async def user_command_color_handler(query: CallbackQuery, callback_data: UserCallback) -> None:
        label, price, style, colors = await parse_data(url=order.url)
        await bot.send_message(
                chat_id=query.from_user.id,
                text="Выберите цвет: ",
                reply_markup=create_colors_keyboard(colors)
            )
        
    @dp.callback_query(UserCallback.filter(F.foo == 'color_choosed'))
    async def user_command_color_choosed_handler(query: CallbackQuery, callback_data: UserCallback) -> None:
        await bot.send_message(
                chat_id=query.from_user.id,
                text="Пожалуйста, подождите, мы получаем информацию с сайта.\nЭто может занять некоторое время."
            )
        order.color = callback_data.option
        await bot.send_message(
                chat_id=query.from_user.id,
                text=f"Вы выбрали цвет: {order.color}",
                reply_markup=create_keyboard(['size', 'back'])
            )


    @dp.callback_query(UserCallback.filter(F.foo == 'last_step'))
    async def user_command_last_handler(query: CallbackQuery, callback_data: UserCallback) -> None:
        d_flag = '!f' if order.delivery_type[0] == 'Б' else '!c'
        price = await calculate_parsed(str(order.price), d_flag)
        order.price = float(price)
        await bot.send_message(
                chat_id=query.from_user.id,
                text=await command_last_message(order, order.label, order.style, price),
                reply_markup=create_keyboard(['confirm', 'back'])
            )
        flags.clear()
        
    @dp.callback_query(UserCallback.filter(F.foo == 'confirm'))
    async def user_command_confirm_handler(query: CallbackQuery, callback_data: UserCallback) -> None:
        order.user = '@' + query.from_user.username
        order.status = 'created'
        cur = con.cursor()
        tz = pytz.timezone("Europe/Moscow")
        order.date = str(datetime.now(tz))
        while True:
            order.id = random.randint(999, 100000)
            if all(row[0] != order.id for row in cur.execute("SELECT id FROM orders WHERE status != 'canceled'")):
                break
        cur.execute('INSERT INTO orders VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (order.id, order.user, query.from_user.id, order.category, order.url, order.price, order.delivery_type, order.address, order.size, order.label, order.style, order.status, order.color, order.date))
        con.commit()
        cur.close()
        await bot.send_message(
                chat_id=query.from_user.id,
                text=await command_confirm_message(order),
            )
        await bot.send_message(
                chat_id=admin.id,
                text=await command_confirm_order_admin_message(order),
                reply_markup=create_keyboard_admin(['all_active_orders'])
            )
    
    @dp.callback_query(UserCallback.filter(F.foo == 'my_orders'))
    async def user_command_my_orders_handler(query: CallbackQuery, callback_data: UserCallback) -> None:
        user_id = query.from_user.id
        cur = con.cursor()
        orders = cur.execute(f"SELECT id FROM orders WHERE userID == {user_id}")
        orders = orders.fetchall()
        cur.close()
        if len(orders) == 0:
            text = "Вы еще не делали заказов."
        else:
            text = "Активные заказы: "
        await bot.send_message(
                chat_id=query.from_user.id,
                text=text,
                reply_markup=create_user_orders_keyboard(orders)
            )
    
    @dp.callback_query(UserCallback.filter(F.foo.contains('active_')))
    async def user_command_active_orders_handler(query: CallbackQuery, callback_data: UserCallback) -> None:
        id = callback_data.foo.split("_")[1]
        cur = con.cursor()
        cur.execute(f"SELECT * FROM orders WHERE id == {id}")
        order = cur.fetchone()
        cur.close()
        if order[11] == 'confirmed':
            markup = create_user_events(['cancel_order', 'pay'], id)
        else:
            markup = create_user_events(['cancel_order'], id)
        await bot.send_message(
                chat_id=query.from_user.id,
                text=await command_active_order_user_message(order),
                reply_markup=markup
            )
        
    @dp.callback_query(UserCallback.filter(F.foo.contains('cancel_')))
    async def user_command_cancel_order_handler(query: CallbackQuery, callback_data: UserCallback) -> None:
        id = callback_data.foo.split("_")[1]
        cur = con.cursor()
        cur.execute(f"UPDATE orders SET status = 'canceled' WHERE id == {id}")
        con.commit()
        cur.execute(f"SELECT * FROM orders WHERE id == {id}")
        order = cur.fetchone()
        cur.close()
        await bot.send_message(
                chat_id=query.from_user.id,
                text=await command_cancel_confirmed_message(order),
            )
        await bot.send_message(
                chat_id=admin.id,
                text=await command_cancel_admin_message(order) + '\nПользователь отменил заказ.',
            )
        
    @dp.callback_query(UserCallback.filter(F.foo.contains('pay_')))
    async def user_command_pay_handler(query: CallbackQuery, callback_data: UserCallback) -> None:
        id = callback_data.foo.split("_")[1]
        flags.push(f"!o!p{id}")
        await bot.send_message(
                chat_id=query.from_user.id,
                text=f"Для оплаты заказа {id} переведите сумму, указанную в деталях заказа на номер карты: ,\n после чего пришлите скриншот перевода боту для подьверждения оплаты.",
            )
        

    # Admin callbacks
    @dp.callback_query(AdminCallback.filter(F.foo == 'all_active_orders'))
    async def admin_command_all_active_orders_handler(query: CallbackQuery, callback_data: AdminCallback) -> None:
        cur = con.cursor()
        orders = cur.execute("SELECT id FROM orders WHERE status != 'canceled' AND status != 'shipped'")
        orders = orders.fetchall()
        cur.close()
        if len(orders) == 0:
            text = "В данный момент нет активных заказов."
        else:
            text = "Активные заказы: "
        await bot.send_message(
                chat_id=admin.id,
                text=text,
                reply_markup=create_active_orders_keyboard(orders)
            )
    
    @dp.callback_query(AdminCallback.filter(F.foo.contains('active_')))
    async def admin_command_active_handler(query: CallbackQuery, callback_data: AdminCallback) -> None:
        id = callback_data.foo.split("_")[1]
        cur = con.cursor()
        cur.execute(f"SELECT * FROM orders WHERE id == {id}")
        order = cur.fetchone()
        cur.close()
        if order[11] == 'created':
            markup = create_admin_events(['confirm_order', 'cancel_order'], int(id))
        else:
            markup = create_admin_events(['cancel_order', 'confirm_shipping'], int(id))
        await bot.send_message(
                chat_id=admin.id,
                text=await command_order_admin_message(order),
                reply_markup=markup
            )

    @dp.callback_query(AdminCallback.filter(F.foo.contains('confirm_order_')))
    async def admin_command_confirm_order_handler(query: CallbackQuery, callback_data: AdminCallback) -> None:
        id = int(callback_data.foo.split("_")[2])
        cur = con.cursor()
        cur.execute(f"UPDATE orders SET status = 'confirmed' WHERE id == {id}")
        con.commit()
        cur.execute(f"SELECT * FROM orders WHERE id == {id}")
        order = cur.fetchone()
        cur.close()
        await bot.send_message(
                chat_id=admin.id,
                text=await command_confirm_admin_message(order),
                reply_markup=create_keyboard_admin(['all_active_orders', 'canceled_orders'])
            )
        await bot.send_message(
                chat_id=order[2],
                text=await command_order_confirmed_message(order),
                reply_markup=create_keyboard(['my_orders'])
            )
    
    @dp.callback_query(AdminCallback.filter(F.foo.contains('cancel_')))
    async def admin_command_cancel_order_handler(query: CallbackQuery, callback_data: AdminCallback) -> None:
        id = int(callback_data.foo.split("_")[1])
        cur = con.cursor()
        cur.execute(f"UPDATE orders SET status = 'canceled' WHERE id == {id}")
        con.commit()
        cur.execute(f"SELECT * FROM orders WHERE id == {id}")
        order = cur.fetchone()
        cur.close()
        await bot.send_message(
                chat_id=admin.id,
                text=await command_cancel_admin_message(order),
                reply_markup=create_keyboard_admin(['all_active_orders', 'canceled_orders'])
            )
        await bot.send_message(
                chat_id=order[2],
                text=await command_cancel_confirmed_message(order),
                reply_markup=create_keyboard(['my_orders'])
            )
        
    @dp.callback_query(AdminCallback.filter(F.foo.contains('show_info_')))
    async def admin_command_show_info_handler(query: CallbackQuery, callback_data: AdminCallback) -> None:
        id = int(callback_data.foo.split("_")[2])
        cur = con.cursor()
        cur.execute(f"SELECT * FROM orders WHERE id == {id}")
        order = cur.fetchone()
        cur.close()
        if order[11] == 'canceled' or order[11] == 'shipped':
            markup = create_admin_events(['delete_canceled'], id)
        else:
            markup = create_admin_events(['confirm_payment', 'decline_payment'], id)
        await bot.send_message(
                chat_id=admin.id,
                text=await command_order_admin_message(order),
                reply_markup=markup
            )

    @dp.callback_query(AdminCallback.filter(F.foo.contains('confirm_payment_')))
    async def admin_command_confirm_order_payment_handler(query: CallbackQuery, callback_data: AdminCallback) -> None:
        id = int(callback_data.foo.split("_")[2])
        cur = con.cursor()
        cur.execute(f"UPDATE orders SET status = 'paid' WHERE id == {id}")
        con.commit()
        cur.execute(f"SELECT * FROM orders WHERE id == {id}")
        order = cur.fetchone()
        cur.close()
        await bot.send_message(
                chat_id=admin.id,
                text=await command_payment_confirmed_admin(order),
            )
        await bot.send_message(
                chat_id=order[2],
                text=await command_payment_confirmed_user(order),
                reply_markup=create_keyboard(['ask'])
            )

    @dp.callback_query(AdminCallback.filter(F.foo.contains('decline_payment_')))
    async def admin_command_decline_order_payment_handler(query: CallbackQuery, callback_data: AdminCallback) -> None:
        id = int(callback_data.foo.split("_")[2])
        cur = con.cursor()
        cur.execute(f"SELECT * FROM orders WHERE id == {id}")
        order = cur.fetchone()
        cur.close()
        await bot.send_message(
                chat_id=admin.id,
                text=await command_payment_declined_admin(order),
            )
        await bot.send_message(
                chat_id=order[2],
                text=await command_payment_declined_user(order),
                reply_markup=create_keyboard(['ask'])
            )

    @dp.callback_query(AdminCallback.filter(F.foo.contains('confirm_shipping_')))
    async def admin_command_confirm_order_shipping_handler(query: CallbackQuery, callback_data: AdminCallback) -> None:
        id = int(callback_data.foo.split("_")[2])
        cur = con.cursor()
        cur.execute(f"UPDATE orders SET status = 'shipped' WHERE id == {id}")
        con.commit()
        cur.execute(f"SELECT * FROM orders WHERE id == {id}")
        order = cur.fetchone()
        cur.close()
        await bot.send_message(
                chat_id=admin.id,
                text=await command_order_shipped_admin(order)
            )
        await bot.send_message(
                chat_id=order[2],
                text=await command_order_shipped_user(order),
                reply_markup=create_keyboard(['ask'])
        )

    @dp.callback_query(AdminCallback.filter(F.foo == 'canceled_orders'))
    async def admin_command_calceled_orders_handler(query: CallbackQuery, callback_data: AdminCallback) -> None:
        cur = con.cursor()
        cur.execute("SELECT * FROM orders WHERE status == 'canceled' OR status == 'shipped'")
        orders = cur.fetchall()
        cur.close()
        if len(orders) == 0:
            text = "В данный момент нет завершенных заказов."
        else:
            text = "Завершенные заказы: "
        await bot.send_message(
                chat_id=admin.id,
                text=text,
                reply_markup=create_canceled_orders_keyboard(orders)
            )

    @dp.callback_query(AdminCallback.filter(F.foo.contains('canceled_')))
    async def admin_command_canceled_order_info_handler(query: CallbackQuery, callback_data: AdminCallback) -> None:
        id = int(callback_data.foo.split("_")[1])
        cur = con.cursor()
        cur.execute(f"SELECT * FROM orders WHERE id == {id}")
        order = cur.fetchone()
        cur.close()
        await bot.send_message(
                    chat_id=admin.id,
                    text=f"Заказ {id}",
                    reply_markup=create_admin_events(['show_info, delete_canceled'], id)
                )
    
    @dp.callback_query(AdminCallback.filter(F.foo.contains('delete_canceled_')))
    async def admin_delete_canceled_order_handler(query: CallbackQuery, callback_data: AdminCallback) -> None:
        id = int(callback_data.foo.split("_")[2])
        cur = con.cursor()
        cur.execute(f"DELETE FROM orders WHERE id == {id}")
        con.commit()
        cur.close()
        await bot.send_message(
                chat_id=admin.id,
                text=f"Заказ {id} успешно удален!",
            )

    # Message handlers
    @dp.message()
    async def message_handler(message : Message) -> None:
        prev = flags.get(-1)
        if prev == '!o!a':
            order.address = message.text
            await bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"Вы ввели адрес: {order.address}.",
                    reply_markup=create_keyboard(['color', 'back'])
                )
            flags.clear()
        elif prev == '!o!u':
            order.url = message.text
            await bot.send_message(
                    chat_id=message.from_user.id,
                    text=f"Вы ввели ссылку: {order.url}.",
                    reply_markup=create_keyboard(['address', 'back'])
                )
            flags.clear()
        elif prev == '!c!f' or prev == '!c!c':
            price = await calculate(message, prev[2] + prev[3])
            await bot.send_message(
                    chat_id=message.from_user.id, 
                    text=f"Цена товара с учетом доставки: {price} руб.",
                    reply_markup=create_keyboard(['create_order', 'back'])
                )
            flags.clear()
        elif prev[0:4] == "!o!p":
            if message.photo:
                # file_name = f"core/database/photos/{message.photo[-1].file_unique_id}:{id}.jpg"
                # await bot.download(file=message.photo[-1].file_id, destination=file_name)
                await bot.send_message(
                    chat_id=admin.id,
                    text=f"Пользователь отправил скриншот с оплатой для заказа {prev[4:]}.\nДля подтверждения оплаты нажмите [посмотреть информацию].",
                    reply_markup=create_admin_events(['show_info'], id=prev[4:])
                )
                await bot.send_photo(
                    chat_id=admin.id,
                    photo=message.photo[-1].file_id
                )
            flags.clear()
