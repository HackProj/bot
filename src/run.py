import asyncio
from aiogram import Bot
import logging

from src.bot.bot_instance import bot, dp
from src.database.database import database_accessor

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s %(asctime)s %(levelname)s %(message)s")


async def startup(bot: Bot):
    logger.info('Bot was started')
    await dp.start_polling(bot)

    await database_accessor.run()


async def shutdown(bot: Bot):
    """Triggers on shutdown"""
    print("govno")
    await database_accessor.stop()
    logger.info("Bot has stopped")


async def main():
    await dp.start_polling(bot, on_startup=startup, on_shutdown=shutdown)


if __name__ == '__main__':
    asyncio.run(main())
