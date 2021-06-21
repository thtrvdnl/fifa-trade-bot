import sys
import time
import email
import imaplib
import numpy as np

from environs import Env
from typing import Optional
from selenium import webdriver

env = Env()
env.read_env()


def get_operating_system() -> str:
    return sys.platform


def get_path_webdriver() -> str:
    system = get_operating_system()
    if system == "linux":
        path = "driver/chromedriver"
    else:
        raise OSError(f"Operating system {system} not supported")

    return path


def get_webdriver() -> Optional[webdriver.Chrome]:
    path_driver = get_path_webdriver()
    webdriver_ = webdriver.Chrome(executable_path=path_driver)
    return webdriver_


def time_sleep(wait: int) -> None:
    wait = np.random.poisson(wait)
    # TODO: сделать усеченное распределение
    wait += (np.sqrt(wait) + np.log(wait))
    time.sleep(wait)


def get_secure_code_by_mail() -> Optional[str]:
    mail = imaplib.IMAP4_SSL(env.str('MAIL'))
    mail.login(env.str('LOGIN'), env.str('PASSWORD'))

    mail.select("inbox")
    result, data = mail.search(None, "ALL")

    id_list = data[0].split()
    latest_email_id = id_list[-1]

    result, data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = data[0][1]
    raw_email_string = raw_email.decode('utf-8')

    email_message = email.message_from_string(raw_email_string)
    body = email_message.get_payload(decode=True).decode('utf-8')
    # TODO: Хардкод
    secure_code = body.split('<span style="color: #000000;"><b>')[2].split('</b></span><br><br>')[0]
    return secure_code


if __name__ == "__main__":
    print(type(get_webdriver()))
