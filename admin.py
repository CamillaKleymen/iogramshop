from aiogram import types
from bot import dp, bot
from aiogram.dispatcher.filters import Command
from config import admin_id

@dp.message_handler(Command('admin'), user_id=admin_id)
async def admin_panel(message: types.Message):
    await message.reply("Welcome to the admin panel.")
