from aiogram.types import ReplyKeyboardMarkup,  KeyboardButton

keyboard1 = KeyboardButton('Каталог')
keyboard2 = KeyboardButton('Добавить событие')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.row(keyboard1, keyboard2)

ask_keyboard1 = KeyboardButton('Выйти из чата')
ask_keyboard2 = KeyboardButton('Посмотреть событие')
ask_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
ask_keyboard.row(ask_keyboard1, ask_keyboard2)

answer_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Выйти из чата'))