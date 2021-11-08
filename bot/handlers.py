import utils
import loader

from . import misc

from aiogram import types


@loader.dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    try:
        status_browser = loader.web_bot.start()
    except Exception as exp:
        # Нельзя чтобы бот падал, но уведомить надо
        print(exp)
        await message.answer(f"Ошибка: {exp}")
    else:
        await message.answer(status_browser)


@loader.dp.message_handler(commands=['player_buy'])
async def player(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    print(message.text)
    # /player_buy Lionel Messi Quality=Bronze Rarity=Rare Position=Defenders ChemistryStyle=Basic Nationality='' League='' Club='' BidPrice=(Min=1,Max=10) BuyNowPrice=(Min=1,Max=10) Numbers=10
    player = misc.parse_player_from_message(message.text)
    print(player)
    loader.web_bot.buy_players(player)

    await message.answer(message.text + 'aaa')
