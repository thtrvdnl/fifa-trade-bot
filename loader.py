import utils
import browser
import logging

from aiogram import Bot, Dispatcher

webdriver = utils.get_webdriver()
web_bot = browser.WebWorker(webdriver)

API_TOKEN = '1965724449:AAEzNT_wqGaWZ886pKSBPaN05M9yjyucDcQ'

# Configure logging
logging.basicConfig(
    level=logging.INFO
)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
