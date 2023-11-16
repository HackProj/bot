import requests
from aiogram import types, Router, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove

from keyboards.temp import make_row_keyboard
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
async def help(message: types.Message, bot: Bot):
    answer = ["Доступные команды: "]
    for command, description in commands:
        answer.append(hcode(f"/{command}") + f" — {description}")

    await message.answer("\n".join(answer))


# registr
class SendRegistr(StatesGroup):
    SendUrl = State()
    SendGameUrl = State()


@router.message(StateFilter(None), Command("add_friend"))
async def send_url(message: types.Message, state: FSMContext):
    await message.answer(
        text="Отправьте ссылку на профиль потенциальной крысы: https://steamcommunity.com/id/<friend_name>",
    )
    await state.set_state(SendRegistr.SendUrl)


@router.message(SendRegistr.SendUrl)
async def get_friend_url(message: types.Message, state: FSMContext):
    print(message.text.lower())
    print(SteamID.from_url(message.text.lower()))

    await state.update_data(FriendUrl=message.text.lower())
    await state.update_data(TelegramId=message.from_user.id)
    print(await state.get_data())
    print(state.storage)
    await message.answer(
        text="Отправьте ссылку на игру за которой следим: `https://store.steampowered.com/app/730`",
    )
    await state.set_state(SendRegistr.SendGameUrl)
    print(state)


@router.message(SendRegistr.SendGameUrl)
async def get_game_url(message: types.Message, state: FSMContext):
    print(message.text.lower())
    print(SteamID.from_url(message.text.lower()))

    await state.update_data(AppUrl=message.text.lower())

    await message.answer(
        text="Круто, мы теперь будем следить за ним. Если эта крыса зайдет в игру, мы тебе напишем",
    )
    # request.post
    await state.clear()


# update status
# ----------------------------------------------------------------------------------------------------------------------
class UpdateStatus(StatesGroup):
    SendFriendUrl = State()
    SendStatus = State()
    Finish = State()


@router.message(StateFilter(None), Command("update"))
async def select_friends(message: types.Message, state: FSMContext):
    # friends = requests.get(f"" , data={"userId":message.from_user.id})
    my_friends = ["name1", "name2"]

    await message.answer(
        text="Выбери крысу.",
        reply_markup=make_row_keyboard(my_friends)

    )
    await state.set_state(UpdateStatus.SendStatus)


listen = ["Да следим крысой", "Не, я ему доверяю крысой"]


@router.message(UpdateStatus.SendStatus)
async def get_friends_url(message: types.Message, state: FSMContext):
    print(message.text)
    # print(SteamID.from_url(message.text.lower()))

    await state.update_data(TelegramId=message.from_user.id)
    await state.update_data(FriendUrl=message.text)

    print(message.text)
    print(await state.get_data())
    print(state.storage)
    await message.answer(
        text="Следим ?",
        reply_markup=make_row_keyboard(listen)
    )
    await state.set_state(UpdateStatus.Finish)


@router.message(UpdateStatus.Finish)
async def finish_state(message: types.Message, state: FSMContext):
    print(message.text)
    # print(SteamID.from_url(message.text.lower()))

    await state.update_data(IsEnabled=message.text == listen[0])

    print(message.text)
    print(await state.get_data())
    print(state.storage)
    await message.answer(
        text="Договорились",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


# remove friend subscription

class RemoveFriend(StatesGroup):
    SendFriendUrl = State()
    Finish = State()


@router.message(StateFilter(None), Command("remove_fined"))
async def select_friends(message: types.Message, state: FSMContext):
    # friends = requests.get(f"" , data={"userId":message.from_user.id})
    my_friends = ["name1", "name2"]

    await message.answer(
        text="Выбери кого выписать из крыс.",
        reply_markup=make_row_keyboard(my_friends)

    )
    await state.set_state(RemoveFriend.SendFriendUrl)


confirmation = ("Да", "Нет")


@router.message(RemoveFriend.SendFriendUrl)
async def work_with_friend_url(message: types.Message, state: FSMContext):
    print(message.text)

    await state.update_data(TelegramId=message.from_user.id)
    await state.update_data(FriendUrl=message.text)

    print(message.text)
    print(await state.get_data())
    print(state.storage)
    await message.answer(
        text=f"Уверен, что хочешь удалить {message.text}",
        reply_markup=make_row_keyboard(confirmation)
    )
    await state.set_state(RemoveFriend.Finish)


@router.message(RemoveFriend.Finish)
async def work_with_friend_url(message: types.Message, state: FSMContext):
    print(message.text)

    if message.text == confirmation[0]:
        #     todo request delete
        await message.answer(
            text=f"Удалили крысу",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            text=f"Окей, тогда оставляем",
            reply_markup=ReplyKeyboardRemove()
        )
    await state.clear()


# Get friends
@router.message(StateFilter(None), Command("friends"))
async def select_friends(message: types.Message, state: FSMContext):
    # friends = requests.get(f"" , data={"userId":message.from_user.id})
    my_friends = ["name1", "name2"]

    await message.answer(
        text=", ".join(my_friends),
        reply_markup=make_row_keyboard(my_friends)

    )


# Get friends games
class GetFriendsGames(StatesGroup):
    SendFriendUrl = State()
    Finish = State()


@router.message(StateFilter(None), Command("friend_games"))
async def select_friends(message: types.Message, state: FSMContext):
    # friends = requests.get(f"" , data={"userId":message.from_user.id})
    my_friends = ["name1", "name2"]
    a = f'Выбери друга {", ".join(my_friends)}'
    await message.answer(

        text=f'Выбери друга ',
        reply_markup=make_row_keyboard(my_friends)
    )

    await state.set_state(GetFriendsGames.SendFriendUrl)


@router.message(GetFriendsGames.SendFriendUrl)
async def return_games(message: types.Message, state: FSMContext):
    #     todo request
    games = ["CS2", "Dota2", "PUBG"]

    await message.answer(
        text=f'Мы следим у него за {", ".join(games)}',
        reply_markup=ReplyKeyboardRemove()
    )

    await state.clear()
