import asyncio
from config import bot_token
from aiogram import Bot, Dispatcher, executor

loop = asyncio.new_event_loop()
bot = Bot(bot_token, parse_mode='HTML')
dp = Dispatcher(bot, loop=loop)

if __name__ == '__main__':
    from handler import dp
    executor.start_polling(dp)