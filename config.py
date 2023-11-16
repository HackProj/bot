from aiogram import Bot, Dispatcher
import os
from environs import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

BASE_DIR = os.path.dirname(__file__)





