from aiogram import types, Router, Bot
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hcode
from src.bot.messages import START
from src.bot.bot_instance import dp
from src.bot.handlers.commands import commands

router = Router()

print("here")


@dp.message(CommandStart())
async def start(message: types.Message, bot: Bot):
    await message.answer(text=START)


@dp.message(commands=["test"])
async def commands(message: types.Message):
    answer = ["Доступные команды: "]
    for command, description in commands:
        answer.append(hcode(f"/{command}") + f" — {description}")

    await message.answer("\n".join(answer))


@dp.message()
async def echo_handler(message: types.Message) -> None:
    try:
        print(123)
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")
