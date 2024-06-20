# handlers.py
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from bot import dp, bot
from text import *
from states import Registration
import buttons as bt
import database as db

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    check = await db.check_user(user_id)
    prods = await db.get_pr()
    if check:
        await message.reply(WELCOME_MESSAGE, reply_markup=types.ReplyKeyboardRemove())
        await message.reply(CHOOSE_PRODUCT, reply_markup=bt.main_menu_buttons(prods))
    else:
        await message.reply(REGISTRATION_PROMPT, reply_markup=types.ReplyKeyboardRemove())
        await Registration.waiting_for_name.set()

@dp.message_handler(state=Registration.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    user_name = message.text
    await state.update_data(user_name=user_name)
    await message.reply(SEND_NUMBER_PROMPT, reply_markup=bt.num_button())
    await Registration.waiting_for_number.set()

@dp.message_handler(state=Registration.waiting_for_number, content_types=types.ContentType.CONTACT)
async def process_number(message: types.Message, state: FSMContext):
    user_number = message.contact.phone_number
    await state.update_data(user_number=user_number)
    await message.reply(SEND_LOCATION_PROMPT, reply_markup=bt.loc_button())
    await Registration.waiting_for_location.set()

@dp.message_handler(state=Registration.waiting_for_location, content_types=types.ContentType.LOCATION)
async def process_location(message: types.Message, state: FSMContext):
    user_location = (message.location.latitude, message.location.longitude)
    user_data = await state.get_data()
    user_name = user_data['user_name']
    user_number = user_data['user_number']
    await db.save_user(message.from_user.id, user_name, user_number, user_location)
    await message.reply(REGISTRATION_COMPLETE, reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
