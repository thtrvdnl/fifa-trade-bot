import utils
import browser
import logging

from aiogram import Bot, Dispatcher

webdriver = utils.get_webdriver()
web_bot = browser.WebWorker(webdriver)

API_TOKEN = utils.env.str("TOKEN")

# Configure logging
logging.basicConfig(
    level=logging.INFO
)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
