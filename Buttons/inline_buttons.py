from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def delete_event_inline(event_id):
    delete_event = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Удалить событие',
                                                                              callback_data='delete_event_id:' + str(
                                                                                  event_id)
                                                                              ))
    return delete_event


cansel_add_event = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='❌ Отменить операцию',
                                                                              callback_data='stop'))
time_empty = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Оставить пустым',
                                                                        callback_data='time_empty'))

# delete_event = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Удалить событие',
#                                                                           callback_data='delete_event'))
