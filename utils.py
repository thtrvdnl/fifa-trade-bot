import re
import sys
import time
import email
import imaplib
import logging
import functools
import numpy as np

from environs import Env
from selenium import webdriver
from dataclasses import dataclass
from email.message import Message
from typing import Optional, Tuple, Union
from selenium.webdriver.chrome.options import Options

import excepts

env = Env()
env.read_env()


@dataclass
class Player:
    name: str
    quality: str
    rarity: str
    position: str
    chemistry_style: str
    nationality: str
    league: str
    club: str
    bid_price: str
    buy_now_price: str
    numbers: str
    step_buy: int = 10

    def get_prices(self, attr) -> tuple[Union[int, str], Union[int, str]]:
        print(getattr(self, attr))
        prices = getattr(self, attr).split(',')

        def find_number(price: str) -> list[str]:
            return re.findall(r'\d+', price)

        price_min = int(*find_number(prices[0])) if find_number(prices[0]) else ''
        price_max = int(*find_number(prices[1])) if find_number(prices[1]) else ''

        return price_min, price_max


def get_operating_system() -> str:
    return sys.platform


def get_path_webdriver() -> str:
    system = get_operating_system()
    if system == "linux":
        path = "driver/chromedriver"
    else:
        raise OSError(f"Operating system {system} not supported")

    return path


def set_user_agent() -> Options:
    options = Options()
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--start-maximized")
    return options


def get_webdriver() -> webdriver.Chrome:
    options = set_user_agent()
    path_driver = get_path_webdriver()
    webdriver_ = webdriver.Chrome(executable_path=path_driver, chrome_options=options)
    return webdriver_


def time_sleep(wait: int) -> None:
    wait = np.random.poisson(wait)
    # TODO: сделать усеченное распределение
    time.sleep(wait)


def get_secure_code_by_mail() -> str:
    mail = imaplib.IMAP4_SSL(env.str("MAIL"))
    mail.login(env.str("LOGIN"), env.str("PASSWORD"))

    mail.select("inbox")
    result, data = mail.search(None, "ALL")

    id_list = data[0].split()
    latest_email_id = id_list[-1]

    result, data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = data[0][1]
    raw_email_string = raw_email.decode("utf-8")

    email_message = email.message_from_string(raw_email_string)
    if sender_verification("EA", email_message):
        body = str(email_message.get_payload()[1])
        # TODO: Хардкод
        secure_code = body.split('<span style="color: #000000;"><b>')[2].split(
            "</b></span><br><br>"
        )[0]
        return secure_code


def sender_verification(name: str, message: Message) -> bool:
    senders = email.utils.parseaddr(message["From"])
    for sender in senders:
        if name not in sender:
            raise excepts.SenderError
    return True


def situations_have_changed(param: str, check_param: Union[str, bool]) -> str:
    # Изменения на сайте FIFA, который вызывают исключения
    if param == 'Chemistry Style':
        check_param = check_param.upper() if isinstance(check_param, str) else False

    return check_param


def print_func(func):
    """Print start/stop for function."""

    @functools.wraps(func)
    def func_(*args, **kwargs):
        print(f"Start: {func.__qualname__}")
        result = func(*args, **kwargs)
        print(f"Stop: {func.__qualname__}")
        return result

    return func_


if __name__ == "__main__":
    print(get_secure_code_by_mail())
