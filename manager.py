import bot
import loader

from aiogram import executor

"""
Запускает систему в которой:
- единственный бразуер
- единственный бот
"""

executor.start_polling(loader.dp, on_startup=bot.on_startup)

