from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from typing import Dict, Awaitable, Callable, Any

from src.bot.bot_instance import  dp

class GetUserInHandler(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]) -> Any:

        if event.inline_query:
            user_id = event.inline_query.message.from_user.id
        elif event.message:
            user_id = event.message.from_user.id
        else:
            return await handler(event, data)

        # user = await Users.get_user(user_id)
        # if not user:
        #     await Users.create_user(user_id)
        #     user = await Users.get_user(user_id)
        #
        # data['user'] = user
        # return await handler(event, data)

dp.update.middleware.register(GetUserInHandler())