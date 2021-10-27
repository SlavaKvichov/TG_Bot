from aiogram.types import ReplyKeyboardMarkup,  KeyboardButton

keyboard1 = KeyboardButton('Каталог')
keyboard2 = KeyboardButton('Добавить событие')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row(keyboard1, keyboard2)

answer_keyboard1 = KeyboardButton('Выйти из чата')
answer_keyboard2 = KeyboardButton('Посмотреть событие')
answer_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
answer_keyboard.row(answer_keyboard1, answer_keyboard2)