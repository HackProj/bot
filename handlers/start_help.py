import json

import requests
from aiogram import Bot, F, Router, types
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hcode

from config import dp
from handlers.commands import commands
from keyboards.temp import make_row_keyboard
from messages import START

router = Router()
dp.include_router(router)
API_PATH = "http://localhost:6001/api/"
headers = {"Content-type": "application/json", "Accept": "application/json"}


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


class SendRegistr(StatesGroup):
    SendUrl = State()
    SendGameUrl = State()


@router.message(StateFilter(None), Command("add_friend"))
async def send_url(message: types.Message, state: FSMContext):
    await message.answer(
        text="Отправьте ссылку на профиль потенциальной крысы",
    )
    await state.set_state(SendRegistr.SendUrl)


@router.message(SendRegistr.SendUrl)
async def get_friend_url(message: types.Message, state: FSMContext):
    await state.update_data(FriendUrl=message.text.lower())
    await state.update_data(TelegramId=message.from_user.id)
    await message.answer(
        text="Отправьте ссылку на игру за которой следим: `https://store.steampowered.com/app/730`",
    )
    await state.set_state(SendRegistr.SendGameUrl)


@router.message(SendRegistr.SendGameUrl)
async def get_game_url(message: types.Message, state: FSMContext):
    await state.update_data(AppUrl=message.text)
    requests_data = requests.post(
        f"{API_PATH}Users/subscribe",
        data=json.dumps(await state.get_data()),
        headers=headers,
    )
    if requests_data.status_code == 415:
        await message.answer(
            text="Проблема, либо у крысы нет этой игры или закрытый профиль 🐀",
        )
    elif requests_data.status_code >= 400:
        await message.answer(
            text=f"Проблема, {requests_data.text}",
        )
    else:
        await message.answer(
            text="Круто, мы теперь будем следить за ним. Если эта крыса зайдет в игру, мы тебе напишем",
        )
    await state.clear()


class UpdateStatus(StatesGroup):
    SendFriendUrl = State()
    SendStatus = State()
    Finish = State()


@router.message(StateFilter(None), Command("update"))
async def select_friends(message: types.Message, state: FSMContext):
    friends_names = requests.get(
        f"{API_PATH}Users/subscriptions?userId={message.from_user.id}"
    )

    friend_dict = {}
    for elem in friends_names.json():
        friend_dict[elem["friendName"]] = elem["profileUrl"]

    await state.update_data(FriendsDict=friend_dict)
    await message.answer(
        text="Выбери крысу.", reply_markup=make_row_keyboard(friend_dict.keys())
    )
    await state.set_state(UpdateStatus.SendStatus)


listen = ["Да следим крысой", "Не, я ему доверяю крысой"]


@router.message(UpdateStatus.SendStatus)
async def get_friends_url(message: types.Message, state: FSMContext):
    friends_dict = (await state.get_data()).get("FriendsDict", None)

    await state.update_data(TelegramId=message.from_user.id)
    await state.update_data(FriendUrl=friends_dict.get(message.text))

    await message.answer(text="Следим ?", reply_markup=make_row_keyboard(listen))
    await state.set_state(UpdateStatus.Finish)


@router.message(UpdateStatus.Finish)
async def finish_state(message: types.Message, state: FSMContext):
    await state.update_data(IsEnabled=message.text == listen[0])
    data = requests.put(
        f"{API_PATH}", data=json.dumps(await state.get_data()), headers=headers
    )

    await message.answer(text="Договорились", reply_markup=ReplyKeyboardRemove())
    await state.clear()


class RemoveFriend(StatesGroup):
    SendFriendUrl = State()
    Finish = State()


@router.message(StateFilter(None), Command("remove_fined"))
async def select_friends(message: types.Message, state: FSMContext):
    friend_dict = dict()
    friends_names = requests.get(
        f"{API_PATH}Users/subscriptions?userId={message.from_user.id}"
    )

    for elem in friends_names.json():
        friend_dict[elem["friendName"]] = elem["profileUrl"]

    await state.update_data(FriendsDict=friend_dict)

    await message.answer(
        text="Выбери кого выписать из крыс.",
        reply_markup=make_row_keyboard(friend_dict.keys()),
    )
    await state.set_state(RemoveFriend.SendFriendUrl)


confirmation = ("Да", "Нет")


@router.message(RemoveFriend.SendFriendUrl)
async def work_with_friend_url(message: types.Message, state: FSMContext):
    friends_dict = (await state.get_data()).get("FriendsDict", None)

    await state.update_data(TelegramId=message.from_user.id)
    await state.update_data(FriendUrl=friends_dict[message.text])

    await message.answer(
        text=f"Уверен, что хочешь удалить {message.text}",
        reply_markup=make_row_keyboard(confirmation),
    )
    await state.set_state(RemoveFriend.Finish)


@router.message(RemoveFriend.Finish)
async def work_with_friend_url(message: types.Message, state: FSMContext):
    if message.text == confirmation[0]:
        data = requests.delete(
            f"{API_PATH}Users/subscription/friend",
            data=json.dumps(await state.get_data()),
            headers=headers,
        )
        if data.status_code < 299:
            await message.answer(
                text=f"Удалили крысу", reply_markup=ReplyKeyboardRemove()
            )
        else:
            await message.answer(
                text=f"Какие-то проблемы {data.status_code}   {data.content}",
                reply_markup=ReplyKeyboardRemove(),
            )
    else:
        await message.answer(
            text=f"Окей, тогда оставляем", reply_markup=ReplyKeyboardRemove()
        )
    await state.clear()


@router.message(StateFilter(None), Command("friends"))
async def select_friends(message: types.Message, state: FSMContext):
    friends_names = requests.get(
        f"{API_PATH}Users/subscriptions?userId={message.from_user.id}"
    )
    friends_names = [elem["friendName"] for elem in friends_names.json()]

    await message.answer(
        text=", ".join(friends_names),
    )


class GetFriendsGames(StatesGroup):
    SendFriendUrl = State()
    Finish = State()


@router.message(StateFilter(None), Command("friend_games"))
async def select_friends(message: types.Message, state: FSMContext):
    friend_dict = dict()
    friends_names = requests.get(
        f"{API_PATH}Users/subscriptions?userId={message.from_user.id}"
    )

    for elem in friends_names.json():
        friend_dict[elem["friendName"]] = elem["profileUrl"]

    await state.update_data(FriendsDict=friend_dict)

    await message.answer(
        text=f"Выбери друга", reply_markup=make_row_keyboard(friend_dict.keys())
    )

    await state.set_state(GetFriendsGames.SendFriendUrl)


@router.message(GetFriendsGames.SendFriendUrl)
async def return_games(message: types.Message, state: FSMContext):
    games = ["CS2", "Dota2", "PUBG"]

    await message.answer(
        text=f'Мы следим у него за {", ".join(games)}',
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.clear()


# Get hints
@router.message(StateFilter(None), Command("hints"))
async def get_hints(message: types.Message):
    data = requests.get(url="http://127.0.0.1:8080/hint").json().get("message")
    await message.answer(
        text=data,
    )
