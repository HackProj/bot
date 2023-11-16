import asyncio
import logging

from aiogram import Bot

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(name)s %(asctime)s %(levelname)s %(message)s"
)


async def on_startup(bot: Bot):
    logger.info("Bot was started")


async def main():
    import handlers
    import middlewares
    from config import bot, dp

    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
