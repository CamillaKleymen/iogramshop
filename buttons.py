from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_buttons(products):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for product in products:
        markup.add(KeyboardButton(product))
    return markup

def num_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Send my contact', request_contact=True)
    markup.add(button)
    return markup

def loc_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button = KeyboardButton('Send my location', request_location=True)
    markup.add(button)
    return markup
