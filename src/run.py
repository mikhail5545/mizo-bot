import asyncio
import sqlite3
import logging
from load_dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from sys import stdout
from os import getenv

from core.handle import dp, handle_events





async def __run() -> None:

    load_dotenv()
    TOKEN = getenv("TOKEN")

    bot = Bot(token=TOKEN)

    await handle_events(bot)
    await dp.start_polling(bot)
    


if __name__ == "__main__":

    con = sqlite3.connect('core/database/orders.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE if not exists orders(id, user, userID, category, url, price, delivery_type, address, size, label, style, status, color, date)")
    con.commit()
    con.close()

    logging.basicConfig(level=logging.INFO, stream=stdout)
    asyncio.run(__run())


