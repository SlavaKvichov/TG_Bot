from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import *

service_bot = Bot(token=TOKEN)
service_dp = Dispatcher(service_bot)

executor.start_polling(service_dp, skip_updates=True)

