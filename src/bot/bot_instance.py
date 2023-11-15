from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

import os
from environs import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'), parse_mode=ParseMode.HTML)
dp = Dispatcher()
