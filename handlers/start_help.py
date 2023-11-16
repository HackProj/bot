from aiogram import types, Router, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from messages import START
from config import dp
from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.utils.markdown import hcode
from handlers.commands import commands
from steam.steamid import SteamID

router = Router()
dp.include_router(router)


@router.message(CommandStart())
async def start(message: types.Message, bot: Bot):
    text = START

    await message.answer(text=text)

@router.message(Command("help"))
async def help(message: types.Message , bot: Bot):
    answer = ["Доступные команды: "]
    for command, description in commands:
        answer.append(hcode(f"/{command}") + f" — {description}")

    await message.answer("\n".join(answer))

class SendLogin(StatesGroup):
    SendUrl = State()

@router.message(StateFilter(None), Command("add_friend"))
async def send_url(message: types.Message, state: FSMContext):
    await message.answer(
        text="Отправьте ссылку на профиль стим друга: https://steamcommunity.com/id/<friend_name>",
    )
    await state.set_state(SendLogin.SendUrl)



@router.message(SendLogin.SendUrl)
async def get_url(message: types.Message, state: FSMContext):
    print(message.text.lower())
    print(SteamID.from_url(message.text.lower()))

    await state.update_data(steam_id=message.text.lower())
    print(await state.get_data())
    print(state.storage)
    # await message.answer(/
    #     text="Спасибо. Теперь, пожалуйста, выберите размер порции:",
    # )
    await state.clear()



# https://store.steampowered.com/app/962130




class SendGame(StatesGroup):
    SendGameUrl = State()

@router.message(StateFilter(None), Command("add_game"))
async def send_game_url(message: types.Message, state: FSMContext):
    await message.answer(
        text="Отправьте ссылку на игру в таком виде: `https://store.steampowered.com/app/730`",
    )
    await state.set_state(SendGame.SendGameUrl)



@router.message(SendGame.SendGameUrl)
async def get_url(message: types.Message, state: FSMContext):
    print(message.text.lower())
    # print(SteamID.from_url(message.text.lower()))

    await state.update_data(steam_id=message.text.lower())
    print(await state.get_data())
    print(state.storage)
    # await message.answer(
    #     text="Спасибо. Теперь, пожалуйста, выберите размер порции:",
    # )
    await state.clear()
