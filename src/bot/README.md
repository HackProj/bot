# Aiogram3 Bot Template
В шаблоне используется библеотека `aiogram3`, в качестве базы данных была использована `sqlalchemy`. 

К сожелению sqlalchemy не поддерживает миграции, поэтому советую использовать для этого `alembic`.

Если вы новичек в аиограме советую посмотреть [учебник](https://mastergroosha.github.io/aiogram-3-guide/) @Groosha.

---
## Оглавление

- [Начало работы](#начало-работы)
- [Регистрация хендлеров](#регистрация-хендлеров)
- [Создание мидлвери](#создание-мидлвери)
---
## Начало работы

1. Загрузите шаблон командой: `git clone https://github.com/NotBupyc/aiogram3-bot-template`
2. Зайдите в файл `.env`
```
BOT_TOKEN = YOUR_TOKEN
```
Подставьте токен своего бота

3. Создайте [venv](https://docs.python.org/3/library/venv.html)
4. Установите зависимости из requirements.txt: `pip install -r requirements.txt`
5. Создайте таблицы с помощью `python create_tables.py`
6. Запустите проект командой: `python main.py`
___

## Регистрация хендлеров

1. Зайдите в папку `handlers`
2. Зайдите в папку `users` или `admins`
3. Создайте файл `your_filename.py`
4. Создайте роутер в файле `your_filename.py`

```python
from aiogram import Router
from config import dp

router = Router()
dp.include_router(router)
```

Регистрирование хэндлеров декораторами:

```python
from aiogram.filters import Command
from aiogram import types

@router.message(Command('Your Command'))
async def cmd(message:types.Message):
    await message.reply("Your text")
```
---

## Создание мидлвери

Мидвери хранятся в папке `middlewares`, я уже добавил туда пару своих наработок:
- `GetUserInHandler.py` - с помощью него можно перебросить класс юзера в хендлер. Вот пример:

```py
from db.models import User

@router.message(CommandStart())
async def start(message: types.Message, bot: Bot, user: User):
    pass
```
- `IgnoreBannedUsers.py` - с помощью него бот не будет реагировать на пользователей находившихся в базе игнора

Так же в папке есть файл базовый мидлвери `example_middleware.py`, незнаю пригодиться ли он.

Советую посмотреть гайд у @Groosha как писать мидлверии [тут](https://mastergroosha.github.io/aiogram-3-guide/filters-and-middlewares/)
