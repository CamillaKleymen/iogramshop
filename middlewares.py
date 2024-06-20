from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from config import admin_id

class AccessMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user_id = update.message.from_user.id
            if user_id != admin_id:
                await update.message.reply(ACCESS_DENIED)
                return
