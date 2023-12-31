from aiogram import types

commands: tuple[tuple[str, str], ...] = (
    ("start", "Запуск бота."),
    ("add_friend", "Добавить крысу."),
    ("hints", "Предложение как оскорбить друга котоырй пошел без тебя."),
    ("remove_fined", "Удалить крысу."),
    ("friends", "Мои крысы."),
    ("update", "Вкл/выкл слежения."),
    ("help", "Справка."),
)


async def set_commands(bot):
    await bot.set_my_commands(
        [
            types.BotCommand(command=name, description=description)
            for name, description in commands
        ]
    )
