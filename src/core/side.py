from aiogram.types import Message
from typing import Literal
from core.parse import parse_currency


async def calculate(message: Message, delivery_flag: Literal['!f', '!c']) -> str:
    print(message.text)
    try:
        price = float(message.text)
    except ValueError as eror:
        return "Цена может быть только числом"
    if delivery_flag == '!f':
        return str(price * 100 + 500)
    else:
        return str(price * 100 + 200)
    
async def calculate_parsed(price: str, delivery_flag: Literal['!f', '!c']) -> str:
    currency = await parse_currency("https://www.cbr.ru/currency_base/daily/")
    _price = float(price)
    if delivery_flag == '!f':
        return str(_price * currency + 1500)
    else:
        return str(_price * currency + 1700)