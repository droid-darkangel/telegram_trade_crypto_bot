from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
token_api = ''
qiwi_token = ''

bot = Bot(token_api)
dp = Dispatcher(bot, storage=MemoryStorage())
