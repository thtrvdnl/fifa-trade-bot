import sys
import time
import numpy as np

from typing import Optional
from selenium import webdriver


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


def time_sleep() -> None:
    wait = np.random.poisson(10)
    if wait < 4:
        wait = 12
    time.sleep(wait)


if __name__ == "__main__":
    print(type(get_webdriver()))
