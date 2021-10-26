from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
# from aiogram.types import CallbackQuery
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from Buttons import markup_button, inline_buttons
from SQL import sql_handler
from Service_Bot import config
from config import *

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

EVENT_TEXT = 'Вы создали событие👆👆👆\nДля того, чтобы получать уведомления о сообщениях перейдите в '\
             + config.data['nickname'] + ' и напишите /start'


class FSMEvent(StatesGroup):
    name = State()
    title = State()
    photo = State()
    description = State()
    data_finish = State()


class FSMDelete_event(StatesGroup):
    event_id = State()
    decision = State()


async def show_catalog(message: types.Message, count=None):
    # event_counts = sql_handler.event_count()[0][0] #Количество событий
    events = sql_handler.catalog()
    for i in events:
        button = inline_buttons.answer_inline()
        button = inline_buttons.delete_event_inline(events[i]['event_id'], button) \
            if events[i]['event_user_owner_id'] == message.from_user.id else button
        caption = events[i]['title'] + '\n' + events[i]['description']
        await bot.send_photo(message.from_user.id, events[i]['photo'], caption=caption, reply_markup=button)


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    first_name = message.from_user.first_name
    last_name = ''
    try:
        last_name = message.from_user.last_name
        await bot.send_message(message.from_user.id, 'Добро пожаловать, ' + first_name + ' ' + last_name,
                               reply_markup=markup_button.keyboard)
    except:
        await bot.send_message(message.from_user.id, 'Добро пожаловать, ' + first_name,
                               reply_markup=markup_button.keyboard)
    user_info = {
        'user_tg_id': message.from_user.id,
        'first_name': first_name,
        'last_name': last_name
    }
    sql_handler.add_user_info(user_info)


@dp.message_handler()
async def echo(message: types.Message):
    if message.text == 'Каталог':
        await show_catalog(message)
    elif message.text == 'Добавить событие':
        await FSMEvent.name.set()
        await message.reply('Имя события', reply_markup=inline_buttons.cansel_add_event)
    else:
        await bot.send_message(message.from_user.id, message.text)


@dp.callback_query_handler(text='stop', state='*')
async def cancel_add_event(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Отменено')


@dp.callback_query_handler(text='time_empty', state='*')
async def load_empty_date_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['data_finish'] = ''
        sql_handler.add_event(data)
        CAPTION = data['title'] + '\n\n' + data['description']
        await bot.send_photo(message.from_user.id, data['photo'],
                             caption=CAPTION)
        await bot.send_message(message.from_user.id, EVENT_TEXT)
    await state.finish()


@dp.callback_query_handler(Text(startswith='delete_event_id'))
async def check_delete_event(callback: types.CallbackQuery, state: FSMContext):
    event_id = int(callback['data'].split(':')[1])
    async with state.proxy() as data:
        data['event_id'] = event_id
    await FSMDelete_event.decision.set()
    await bot.send_message(callback.from_user.id, 'Введите "Удалить"')


@dp.message_handler(state=FSMDelete_event.decision)
async def delete_event(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['decision'] = message.text
        event_id = data['event_id']
        if data['decision'] == "Удалить":
            sql_handler.delete_event(event_id)
            await bot.send_message(message.from_user.id, 'Удалено')
        else:
            await bot.send_message(message.from_user.id, 'Событие не удалено')
    await state.finish()


@dp.message_handler(state=FSMEvent.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['event_user_owner_id'] = message.from_user.id
        data['name'] = message.text
    await FSMEvent.next()
    await message.reply('Заголовок')


@dp.message_handler(state=FSMEvent.title)
async def load_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await FSMEvent.next()
    await message.reply('Медиа')


@dp.message_handler(content_types=['photo'], state=FSMEvent.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMEvent.next()
    await message.reply('Описание')


@dp.message_handler(state=FSMEvent.description)
async def load_decription(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMEvent.next()
    await message.reply('Дата окончания', reply_markup=inline_buttons.time_empty)


@dp.message_handler(state=FSMEvent.data_finish)
async def load_date_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['data_finish'] = message.text
        sql_handler.add_event(data)
        CAPTION = data['title'] + '\n\n' + data['description'] + '\n\n' + 'Дата окончания: ' + data['data_finish']
        await bot.send_photo(message.from_user.id, data['photo'],
                             caption=CAPTION)
        await bot.send_message(message.from_user.id, EVENT_TEXT)
    await state.finish()


executor.start_polling(dp, skip_updates=True)