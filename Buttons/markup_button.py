from aiogram.types import ReplyKeyboardMarkup,  KeyboardButton

keyboard1 = KeyboardButton('Каталог')
keyboard2 = KeyboardButton('Добавить событие')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row(keyboard1, keyboard2)