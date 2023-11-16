from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from typing import Dict, Awaitable, Callable, Any
from config import dp


class Middleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]) -> Any:

        return await handler(event, data)


dp.update.middleware.register(Middleware())
# or
# dp.message.middleware.register(Middleware)
