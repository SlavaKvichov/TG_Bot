from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    if message.text == 'Каталог':
        await message.answer('Я над этим работаю')
    if message.text == 'Добавить событие':
        await message.answer('Я над этим работаю')
    # await message.reply(message.text)
    # await bot.send_message(message.from_user.id, message.text)

executor.start_polling(dp, skip_updates=True)