from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from Buttons import markup_button, inline_buttons
from config import *

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


class FSMEvent(StatesGroup):
    name = State()
    title = State()
    photo = State()
    description = State()
    data_finish = State()


@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Добро пожаловать,', reply_markup=markup_button.keyboard)


@dp.message_handler()
async def echo(message: types.Message):
    if message.text == 'Каталог':
        await message.answer('Я над этим работаю')
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
    async with state.proxy() as data:
        await bot.send_message(message.from_user.id, str(data))
    await state.finish()
    await message.answer('Отменено')


@dp.message_handler(state=FSMEvent.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
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
    async with state.proxy() as data:
        await message.reply(str(data))
    await state.finish()


executor.start_polling(dp, skip_updates=True)