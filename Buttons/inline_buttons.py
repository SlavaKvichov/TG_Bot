from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cansel_add_event = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='❌ Отменить операцию',
                                                                              callback_data='stop'))
time_empty = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Оставить пустым',
                                                                              callback_data='time_empty'))