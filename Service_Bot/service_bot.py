from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.deep_linking import get_start_link

from Buttons import markup_button, inline_buttons
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


@service_dp.callback_query_handler(Text(startswith='answer_user'))
async def check_delete_event(callback: types.CallbackQuery, state: FSMContext):
    await FSMAnswer.answer.set()
    event_user_owner_id = int(callback['data'].split(':')[1])
    event_id = int(callback['data'].split(':')[2])
    event_name = callback['data'].split(':')[3]
    user_id = int(callback['data'].split(':')[4])
    user_first_name = callback['data'].split(':')[5]
    user_last_name = '' if callback['data'].split(':')[6] is None else callback['data'].split(':')[6]
    async with state.proxy() as data:
        data['event_info'] = {}
        data['user_info'] = {}
        data['event_info']['event_user_owner_id'] = event_user_owner_id
        data['event_info']['event_id'] = event_id
        data['event_info']['name'] = event_name
        data['user_info']['user_tg_id'] = user_id
        data['user_info']['first_name'] = user_first_name
        data['user_info']['last_name'] = user_last_name
        await service_bot.send_message(callback.from_user.id, 'Вы вошли в чат с '
                                       + data['user_info']['first_name'] + ' ' + data['user_info']['last_name'],
                                       reply_markup=markup_button.answer_keyboard)


@service_dp.callback_query_handler()
async def show_event():
    link = await get_start_link('foo', encode=True)

@service_dp.message_handler(state=FSMAnswer.answer)
async def echo(message: types.Message, state: FSMContext):
    if message.text == 'Выйти из чата':
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await service_bot.send_message(message.from_user.id, 'Вы вышли из чата')
    else:
        async with state.proxy() as data:
            data['ask'] = message.text
            with service_bot.with_token(config.TOKEN):
                await service_bot.send_message(data['user_info']['user_tg_id'],
                                               'Сообщение от владельца события ' + data['event_info']['name']
                                               + '\n' + message.text)


executor.start_polling(service_dp, skip_updates=True)
