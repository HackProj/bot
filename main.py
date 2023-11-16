import asyncio
from aiogram import Bot
import logging

from handlers.commands import set_commands

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s %(asctime)s %(levelname)s %(message)s")


async def on_startup(bot: Bot):
    logger.info('Bot was started')


async def main():
    from config import bot, dp
    import middlewares
    import handlers
    await set_commands(bot)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
