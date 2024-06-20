from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import logging
import middlewares
import handlers
import admin
import database as db
from config import API_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(middlewares.AccessMiddleware())

async def on_startup(dp):
    await db.create_tables()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
