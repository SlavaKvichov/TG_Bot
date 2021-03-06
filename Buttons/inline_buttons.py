from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def delete_event_inline(event_id, button):
    button.add(InlineKeyboardButton(text='Удалить событие', callback_data='delete_event_id:' + str(event_id)))
    return button


def ask_inline(event_id, user_tg_id, flag):
    text = 'Ответить' if flag == 'Ответить' else 'Связаться'
    button = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text=text,
                                                                        callback_data='ask_user:' + str(event_id) +
                                                                                      ':' + str(user_tg_id)))
    return button


def answer_inline(event_user_owner_id, event_id, user_tg_id):
    button = InlineKeyboardMarkup(row_width=1).row(InlineKeyboardButton(text='Ответить',
                                                                        callback_data='answer_user:'
                                                                                      + str(event_user_owner_id)
                                                                                      + ':' + str(event_id)
                                                                                      + ':' + str(user_tg_id)),
                                                   InlineKeyboardButton(text='Посмотреть событие',
                                                                        callback_data='show_event:' + str(event_id)))
    return button


def show_more_events(button, increase, count):
    button1 = InlineKeyboardButton(text='+1', callback_data='show_more_events:1:' + str(count))
    if increase == 1:
        button.row(button1)
    else:
        button2 = InlineKeyboardButton(text='+' + str(increase),
                                       callback_data='show_more_events:+' + str(increase) + ':' + str(count))
        button.row(button1, button2)
    return button


cansel_add_event = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='❌ Отменить операцию',
                                                                              callback_data='stop'))
time_empty = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Оставить пустым',
                                                                        callback_data='time_empty'))