from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
token_api = '5926193762:AAH050ItwoPvGsmPWpK53Rg7xCPpFPcobHE'
qiwi_token = 'eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6Im0yZG9qbC0wMCIsInVzZXJfaWQiOiI3OTUwNTE5Nzk1OSIsInNlY3JldCI6IjRmNmMzYWE5YzdkMzVkMzkyNzI1NjE0NjIzODg2Zjc2YmJiNDVjYjRhYTQ1YmE1N2IxMzRiMzk4NjM2ODkxMjMifX0='

bot = Bot(token_api)
dp = Dispatcher(bot, storage=MemoryStorage())
