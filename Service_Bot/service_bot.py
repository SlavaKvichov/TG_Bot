from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Buttons import markup_button, inline_buttons
from SQL import sql_handler
from Client_Bot import config
from config import *

storage_service = MemoryStorage()

service_bot = Bot(token=TOKEN)
service_dp = Dispatcher(service_bot, storage=storage_service)


class FSMAnswer(StatesGroup):
    event_user_owner_info = State()
    user_info = State()
    event_info = State()
    ask = State()
    answer = State()


@service_dp.message_handler(commands=['start'], state='*')
async def command_start(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    user_info = sql_handler.get_user_info(user_tg_id=message.from_user.id)
    user_info['last_name'] = '' if user_info['last_name'] is None else user_info['last_name']
    await service_bot.send_message(message.from_user.id, 'Здравствуй, ' + user_info['first_name'] + ' ' +
                                   user_info['last_name'], reply_markup=markup_button.hide_keyboard)


@service_dp.callback_query_handler(Text(startswith='show_event'))
async def show_event(callback: types.CallbackQuery):
    event_id = int(callback['data'].split(':')[1])
    event_info = sql_handler.get_event_info(event_id=event_id)
    event_info = event_info['event_info']
    caption = event_info['title'] + '\n' + event_info['description']
    with service_bot.with_token(config.TOKEN):
        await service_bot.send_photo(event_info['event_user_owner_id'], event_info['photo'], caption=caption)


@service_dp.callback_query_handler(Text(startswith='answer_user'))
async def answer(callback: types.CallbackQuery, state: FSMContext):
    await FSMAnswer.answer.set()
    print(callback['data'])
    event_user_owner_id = int(callback['data'].split(':')[1])
    event_user_owner_info = sql_handler.get_user_info(user_tg_id=event_user_owner_id)
    event_id = int(callback['data'].split(':')[2])
    event_info = sql_handler.get_event_info(event_id=event_id)
    user_id = int(callback['data'].split(':')[3])
    user_info = sql_handler.get_user_info(user_tg_id=user_id)
    async with state.proxy() as data:
        data['event_owner_info'] = event_user_owner_info['user_info']
        data['event_info'] = event_info['event_info']
        data['user_info'] = user_info['user_info']
        if data['user_info']['last_name'] is None:
            data['user_info']['last_name'] = ''
        await service_bot.send_message(callback.from_user.id, 'Вы вошли в чат с '
                                       + data['user_info']['first_name'] + ' ' + data['user_info']['last_name'],
                                       reply_markup=markup_button.answer_keyboard)


@service_dp.message_handler(state=FSMAnswer.answer)
async def echo(message: types.Message, state: FSMContext):
    if message.text == 'Выйти из чата':
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await service_bot.send_message(message.from_user.id, 'Вы вышли из чата',
                                       reply_markup=markup_button.hide_keyboard)
    else:
        async with state.proxy() as data:
            data['ask'] = message.text
            with service_bot.with_token(config.TOKEN):
                await service_bot.send_message(data['user_info']['user_tg_id'], 'Сообщение от владельца события '
                                               + data['event_info']['name'] + '\n' + message.text,
                                               reply_markup=inline_buttons.ask_inline(
                                               event_id=data['event_info']['event_id'],
                                               user_tg_id=data['event_info']['event_user_owner_id'],
                                               flag='Ответить'))


executor.start_polling(service_dp, skip_updates=True)