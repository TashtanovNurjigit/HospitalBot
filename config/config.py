from aiogram import Dispatcher
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from decouple import config


storage = MemoryStorage()
TOKEN = config('TOKEN')
ADMIN = config('ADMIN')
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=storage)
