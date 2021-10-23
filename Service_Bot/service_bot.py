from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

executor.start_polling(dp, skip_updates=True)