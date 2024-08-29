from aiogram import html
from core.classes import Order


async def command_start_message(username) -> str:
    answer = f"Привет, {username}!\n"\
                "\n"\
                f"Это бот канала {html.link("Mizo", "https://t.me/MiZo_Moskow")}, тут вы можете:\n"\
                "\n"\
                "Рассчитать стоимость товара.\n"\
                "Оформить заказ.\n"\
                "Отслеживать статус своего заказа.\n"\
                "Связаться с нами.\n"\
                "\n"\
                "Приятных покупок!"
        
    return answer


async def command_calculate_message() -> str:
    answer = f"{html.bold("Рассчет стоимости товара.")}\n"\
            "\n"\
            "Введите стоимость товара в юанях.\n"
    
    return answer


async def command_address_message() -> str:
    answer = "Укажите адрес для доставки вашего заказа в формате: \n"\
                "г. Москва, ул. Мосфильмовская, д. 10, к. 2, 1122825"
    
    return answer


async def command_url_message() -> str:
    answer = "Введите ссылку на товар с Poizon\n"\
            "Вводите ссылку внимательно! Это важно."

    return answer


async def command_last_message(order: Order, label, style, price) -> str:
    answer = "Введенная вами информация: \n"\
                f"Категория: {order.category}\n"\
                f"Тип доставки: {order.delivery_type}\n"\
                f"Адрес: {order.address}\n"\
                f"Размер: {order.size}\n"\
                f"Цвет: {order.color}\n"\
                f"Информация о товаре: {label}, {style}\n"\
                f"Итоговая цена с доставкой: {price} руб."
    
    return answer
    

async def command_confirm_message(order: Order) -> str:
    answer = f"Спасибо! Заказ {order.id} от {order.date} успешно создан!\n"\
            f"Детали заказа: \n"\
            f"Категория: {order.category}\n"\
            f"Тип доставки: {order.delivery_type}\n"\
            f"Адрес: {order.address}\n"\
            f"Размер: {order.size}\n"\
            f"Цвет: {order.color}\n"\
            f"Информация о товаре: {order.label}, {order.style}\n"\
            f"Итоговая цена с доставкой: {order.price} руб.\n"\
            f"Когда заказ будет подтвержден, вам придет оповещение."
    
    return answer


async def command_confirm_order_admin_message(order: Order) -> str:
    answer = f"Заказ {order.id} от {order.date} от пользователя {order.user}\n"\
            f"Детали заказа: \n"\
            f"Категория: {order.category}\n"\
            f"Тип доставки: {order.delivery_type}\n"\
            f"Адрес: {order.address}\n"\
            f"Размер: {order.size}\n"\
            f"Цвет: {order.color}\n"\
            f"Информация о товаре: {order.label}, {order.style}\n"\
            f"Ссылка на товар: {order.url}\n"\
            f"Итоговая цена с доставкой: {order.price} руб.\n"\
            f"Статус заказа: {order.status}"
    
    return answer


async def command_order_admin_message(order) -> str:
    answer = f"Заказ {order[0]} от пользователя {order[1]} (id: {order[2]}) от {order[13]}\n"\
            f"Детали заказа: \n"\
            f"Категория: {order[3]}\n"\
            f"Тип доставки: {order[6]}\n"\
            f"Адрес: {order[7]}\n"\
            f"Размер: {order[8]}\n"\
            f"Цвет: {order[12]}\n"\
            f"Информация о товаре: {order[9]}, {order[10]}\n"\
            f"Ссылка на товар: {order[4]}\n"\
            f"Итоговая цена с доставкой: {order[5]} руб.\n"\
            f"Статус заказа: {order[11]}"

    return answer


async def command_confirm_admin_message(order) -> str:
    answer = f"Заказ {order[0]} от пользователя {order[1]} (id: {order[2]}) от {order[13]}\nуспешно ПОДТВЕРЖДЕН\n"\
            f"Детали заказа: \n"\
            f"Категория: {order[3]}\n"\
            f"Тип доставки: {order[6]}\n"\
            f"Адрес: {order[7]}\n"\
            f"Размер: {order[8]}\n"\
            f"Цвет: {order[12]}\n"\
            f"Информация о товаре: {order[9]}, {order[10]}\n"\
            f"Ссылка на товар: {order[4]}\n"\
            f"Итоговая цена с доставкой: {order[5]} руб.\n"\
            f"Статус заказа: {order[11]}"

    return answer


async def command_order_confirmed_message(order) -> str:
    answer = f"Ваш заказ {order[0]} от {order[13]} подтвержден! Благодарим за ожидание!\n"\
            f"Детали заказа: \n"\
            f"Категория: {order[3]}\n"\
            f"Тип доставки: {order[6]}\n"\
            f"Адрес: {order[7]}\n"\
            f"Размер: {order[8]}\n"\
            f"Информация о товаре: {order[9]}, {order[10]}\n"\
            f"Ссылка на товар: {order[4]}\n"\
            f"Итоговая цена с доставкой: {order[5]} руб.\n"\
            f"Статус заказа: {order[11]}\n"\
            f"Если у вас возникли какие-то вопросы, свяжитесь с нами (кнопка [Задать вопрос])"

    return answer


async def command_cancel_admin_message(order) -> str:
    answer = f"Заказ {order[0]} от пользователя {order[1]} (id: {order[2]}) от {order[13]} \nуспешно ОТМЕНЕН\n"\
            f"Детали заказа: \n"\
            f"Категория: {order[3]}\n"\
            f"Тип доставки: {order[6]}\n"\
            f"Адрес: {order[7]}\n"\
            f"Размер: {order[8]}\n"\
            f"Информация о товаре: {order[9]}, {order[10]}\n"\
            f"Ссылка на товар: {order[4]}\n"\
            f"Итоговая цена с доставкой: {order[5]} руб.\n"\
            f"Статус заказа: {order[11]}"

    return answer


async def command_cancel_confirmed_message(order) -> str:
    answer = f"Ваш заказ {order[0]} от {order[13]} отменен. \nДля уточнения подробностей, свяжитесь с нами.\n"\
            f"Детали заказа: \n"\
            f"Категория: {order[3]}\n"\
            f"Тип доставки: {order[6]}\n"\
            f"Адрес: {order[7]}\n"\
            f"Размер: {order[8]}\n"\
            f"Информация о товаре: {order[9]}, {order[10]}\n"\
            f"Ссылка на товар: {order[4]}\n"\
            f"Итоговая цена с доставкой: {order[5]} руб.\n"\
            f"Статус заказа: {order[11]}\n"\
            f"Если у вас возникли какие-то вопросы, свяжитесь с нами (кнопка [Задать вопрос])"

    return answer


async def command_active_order_user_message(order) -> str:
    answer = f"Заказ {order[0]} от {order[13]}\n"\
            f"Детали заказа: \n"\
            f"Категория: {order[3]}\n"\
            f"Тип доставки: {order[6]}\n"\
            f"Адрес: {order[7]}\n"\
            f"Размер: {order[8]}\n"\
            f"Информация о товаре: {order[9]}, {order[10]}\n"\
            f"Ссылка на товар: {order[4]}\n"\
            f"Итоговая цена с доставкой: {order[5]} руб.\n"\
            f"Статус заказа: {order[11]}\n"\
            f"Если у вас возникли какие-то вопросы, свяжитесь с нами (кнопка [Задать вопрос])\n"\
            f"Вы можете оплатить заказ сейчас, нажав кнопку [Оплатить заказ],\n или же оплатить заказ при получении."

    return answer


async def command_payment_confirmed_admin(order) -> str:
    answer = f"Заказ {order[0]} от пользователя {order[1]} (id: {order[2]}) от {order[13]}\nуспешно ОПЛАЧЕН\n"\
            f"Детали заказа: \n"\
            f"Категория: {order[3]}\n"\
            f"Тип доставки: {order[6]}\n"\
            f"Адрес: {order[7]}\n"\
            f"Размер: {order[8]}\n"\
            f"Информация о товаре: {order[9]}, {order[10]}\n"\
            f"Ссылка на товар: {order[4]}\n"\
            f"Итоговая цена с доставкой: {order[5]} руб.\n"\
            f"Статус заказа: {order[11]}"

    return answer


async def command_payment_confirmed_user(order) -> str:
    answer = f"Оплата вашего заказа {order[0]} от {order[13]} подтверждена! Благодарим за ожидание!\n"\
            f"Детали заказа: \n"\
            f"Категория: {order[3]}\n"\
            f"Тип доставки: {order[6]}\n"\
            f"Адрес: {order[7]}\n"\
            f"Размер: {order[8]}\n"\
            f"Информация о товаре: {order[9]}, {order[10]}\n"\
            f"Ссылка на товар: {order[4]}\n"\
            f"Итоговая цена с доставкой: {order[5]} руб.\n"\
            f"Статус заказа: {order[11]}\n"\
            f"Если у вас возникли какие-то вопросы, свяжитесь с нами (кнопка [Задать вопрос])"

    return answer


async def command_payment_declined_admin(order) -> str:
    answer = f"Заказ {order[0]} от пользователя {order[1]} (id: {order[2]}) от {order[13]} \n -> оплата НЕ ПОДТВЕРЖДЕНА\n"\
            f"Детали заказа: \n"\
            f"Категория: {order[3]}\n"\
            f"Тип доставки: {order[6]}\n"\
            f"Адрес: {order[7]}\n"\
            f"Размер: {order[8]}\n"\
            f"Информация о товаре: {order[9]}, {order[10]}\n"\
            f"Ссылка на товар: {order[4]}\n"\
            f"Итоговая цена с доставкой: {order[5]} руб.\n"\
            f"Статус заказа: {order[11]}"

    return answer


async def command_payment_declined_user(order) -> str:
    answer = f"Оплата вашего заказа {order[0]} от {order[13]} не подтверждена.\n"\
            f"Детали заказа: \n"\
            f"Категория: {order[3]}\n"\
            f"Тип доставки: {order[6]}\n"\
            f"Адрес: {order[7]}\n"\
            f"Размер: {order[8]}\n"\
            f"Информация о товаре: {order[9]}, {order[10]}\n"\
            f"Ссылка на товар: {order[4]}\n"\
            f"Итоговая цена с доставкой: {order[5]} руб.\n"\
            f"Статус заказа: {order[11]}\n"\
            f"Если у вас возникли какие-то вопросы, свяжитесь с нами (кнопка [Задать вопрос])"

    return answer


async def command_order_shipped_admin(order) -> str:
    answer = f"Заказ {order[0]} от пользователя {order[1]} (id: {order[2]}) от {order[13]} доставлен\n"\
            f"Детали заказа: \n"\
            f"Категория: {order[3]}\n"\
            f"Тип доставки: {order[6]}\n"\
            f"Адрес: {order[7]}\n"\
            f"Размер: {order[8]}\n"\
            f"Информация о товаре: {order[9]}, {order[10]}\n"\
            f"Ссылка на товар: {order[4]}\n"\
            f"Итоговая цена с доставкой: {order[5]} руб.\n"\
            f"Статус заказа: {order[11]}"

    return answer


async def command_order_shipped_user(order) -> str:
    answer = f"Ваш заказ {order[0]} от {order[13]} доставлен. Благодарим за покупку!\n"\
            f"Детали заказа: \n"\
            f"Категория: {order[3]}\n"\
            f"Тип доставки: {order[6]}\n"\
            f"Адрес: {order[7]}\n"\
            f"Размер: {order[8]}\n"\
            f"Информация о товаре: {order[9]}, {order[10]}\n"\
            f"Ссылка на товар: {order[4]}\n"\
            f"Итоговая цена с доставкой: {order[5]} руб.\n"\
            f"Статус заказа: {order[11]}\n"\
            f"Если у вас возникли какие-то вопросы, свяжитесь с нами (кнопка [Задать вопрос])"

    return answer