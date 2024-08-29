from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.classes import UserCallback, AdminCallback


def create_keyboard(buttons: list[str]) -> InlineKeyboardMarkup:
    """
    buttons : list[str] | ['calculate', 'create_order', 'faq', 'fast_delivery', 'common_delivery', 'back']
    """

    builder = InlineKeyboardBuilder() 
    if 'calculate' in buttons:
        builder.button(text='Рассчитать стоимость', callback_data=UserCallback(foo='delivery_type', bar=1, option=""))
    if 'create_order' in buttons:
        builder.button(text='Оформить заказ', callback_data=UserCallback(foo='create_order', bar=2, option=""))
    if 'faq' in buttons:
        builder.button(text='FAQ', callback_data=UserCallback(foo='faq', bar=3, option=""))
    if 'ask' in buttons:
        builder.button(text='Задать вопрос', url='https://web.telegram.org/k/#@Nikitayoot')
    if 'fast_delivery' in buttons:
        builder.button(text='Быстрая доставка', callback_data=UserCallback(foo='fast_delivery', bar=4, option=""))
    if 'common_delivery' in buttons:
        builder.button(text='Обычная доставка', callback_data=UserCallback(foo='common_delivery', bar=5, option=""))
    if 'back' in buttons:
        builder.button(text='Назад', callback_data=UserCallback(foo='back', bar=6, option=""))
    if 'category' in buttons:
        builder.button(text='Кроссовки', callback_data=UserCallback(foo='category_sneak', bar=7, option=""))
        builder.button(text='Ботинки', callback_data=UserCallback(foo='category_shoes', bar=7, option=""))
        builder.button(text='Толстовки, кофты, легкие куртки', callback_data=UserCallback(foo='category_sweater', bar=7, option=""))
        builder.button(text='Футболки, шорты', callback_data=UserCallback(foo='category_shirt', bar=7, option=""))
        builder.button(text='Штаны, джинсы', callback_data=UserCallback(foo='category_pants', bar=7, option=""))
        builder.button(text='Зимние куртки, пальто', callback_data=UserCallback(foo='category_outwear', bar=7, option=""))
        builder.button(text='Носки, майки, нижнее белье', callback_data=UserCallback(foo='category_underwear', bar=7, option=""))
        builder.button(text='Очки, парфюм, украшения, часы', callback_data=UserCallback(foo='category_glasses', bar=7, option=""))
        builder.button(text='Головные уборы', callback_data=UserCallback(foo='category_head', bar=7, option=""))
        builder.button(text='Маленькие сумки', callback_data=UserCallback(foo='category_small_bag', bar=7, option=""))
        builder.button(text='Большие сумки', callback_data=UserCallback(foo='category_big_bag', bar=7, option=""))
        builder.button(text='Другое', callback_data=UserCallback(foo='category_another', bar=7, option=""))
    if 'address' in buttons:
        builder.button(text='Указать адрес доставки', callback_data=UserCallback(foo='address', bar=8, option=""))
    if 'url' in buttons:
        builder.button(text='Ввести ссылку на товар', callback_data=UserCallback(foo='url', bar=9, option=""))
    if 'last_step' in buttons:
        builder.button(text='Подтвердить', callback_data=UserCallback(foo='last_step', bar=10, option=""))
    if 'size' in buttons:
        builder.button(text='Выбрать размер', callback_data=UserCallback(foo='size', bar=11, option=""))
    if 'color' in buttons:
        builder.button(text="Выбрать цвет", callback_data=UserCallback(foo="color", bar=1, option=""))
    if 'confirm' in buttons:
        builder.button(text='Оформить заказ', callback_data=UserCallback(foo='confirm', bar=12, option=""))
    if 'my_orders' in buttons:
        builder.button(text='Ваши заказы', callback_data=UserCallback(foo='my_orders', bar=13, option=""))
    
    
    builder.adjust(1)

    return builder.as_markup()


def create_user_events(buttons: list[str], id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if 'cancel_order' in buttons:
        builder.button(text='Отменить заказ', callback_data=UserCallback(foo=f'cancel_{id}', bar=1, option=""))
    if 'pay' in buttons:
        builder.button(text='Оплатить заказ', callback_data=UserCallback(foo=f'pay_{id}', bar=2, option=""))
    builder.adjust(1)

    return builder.as_markup()


def create_sizes_keyboard(price) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for s in price:
        builder.button(text=f'{s} : {price[s]}', callback_data=UserCallback(foo=f'size_{s}', bar=12, option=""))
    builder.adjust(1)

    return builder.as_markup()

def create_colors_keyboard(colors) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for color in colors:
        builder.button(text=f"{color}", callback_data=UserCallback(foo="color_choosed", bar=1, option=f"{color}"))
    builder.adjust(1)
    
    return builder.as_markup()

def create_user_orders_keyboard(orders) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for order in orders:
        builder.button(text=f'{order[0]}', callback_data=UserCallback(foo=f'active_{order[0]}', bar=4, option=""))
    builder.adjust(1)

    return builder.as_markup()


# Admin keyboards
def create_keyboard_admin(buttons: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if 'all_active_orders' in buttons:
        builder.button(text='Все активные заказы', callback_data=AdminCallback(foo='all_active_orders', bar=3, option=""))
    if 'canceled_orders' in buttons:
        builder.button(text='Завершенные заказы', callback_data=AdminCallback(foo='canceled_orders', bar=2, option=""))
    builder.adjust(1)

    return builder.as_markup()


def create_active_orders_keyboard(orders) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for order in orders:
        builder.button(text=f'{order[0]}', callback_data=AdminCallback(foo=f'active_{order[0]}', bar=4, option=""))
    builder.adjust(1)

    return builder.as_markup()

def create_canceled_orders_keyboard(orders) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for order in orders:
        builder.button(text=f'{order[0]}', callback_data=AdminCallback(foo=f'calceled_{order[0]}', bar=1, option=""))
    builder.adjust(1)

    return builder.as_markup()


def create_admin_events(buttons: list[str], id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    if 'confirm_order' in buttons:
        builder.button(text=f'Подтвердить заказ {id}', callback_data=AdminCallback(foo=f'confirm_order_{id}', bar=12, option=""))
    if 'cancel_order' in buttons:
        builder.button(text=f'Отменить заказ {id}', callback_data=AdminCallback(foo=f'calcel_{id}', bar=13, option=""))
    if 'show_info' in buttons:
        builder.button(text='Посмотреть информацию', callback_data=AdminCallback(foo=f'show_info_{id}', bar=14, option=""))
    if 'confirm_payment' in buttons:
        builder.button(text='Подтвердить оплату', callback_data=AdminCallback(foo=f'confirm_payment_{id}', bar=1, option=""))
    if 'decline_payment' in buttons:
        builder.button(text='Отклонить оплату', callback_data=AdminCallback(foo=f'decline_payment_{id}', bar=2, option=""))
    if 'confirm_shipping' in buttons:
        builder.button(text='Подтвердить доставку заказа', callback_data=AdminCallback(foo=f'confirm_shipping_{id}', bar=2, option=""))
    if 'delete_canceled' in buttons:
        builder.button(text=f'Удалить заказ {id}', callback_data=AdminCallback(foo=f'delete_canceled_{id}', bar=14, option=""))
    builder.adjust(1)

    return builder.as_markup()
