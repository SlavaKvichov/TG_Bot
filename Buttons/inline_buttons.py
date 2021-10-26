from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def delete_event_inline(event_id, button):
    button.add(InlineKeyboardButton(text='Удалить событие', callback_data='delete_event_id:' + str(event_id)))
    return button


def answer_inline():
    button = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Ответить', callback_data='answer_user'))
    return button


cansel_add_event = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='❌ Отменить операцию',
                                                                              callback_data='stop'))
time_empty = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Оставить пустым',
                                                                        callback_data='time_empty'))