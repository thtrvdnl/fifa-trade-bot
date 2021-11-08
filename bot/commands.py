from aiogram import types


async def on_startup(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("player_buy", "Закупить игрока"),
            types.BotCommand("players", "Закупить игрока"),
        ]
    )
