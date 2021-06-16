import sys

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
    driver = webdriver.Chrome(executable_path=path_driver)
    return driver


if __name__ == "__main__":
    print(type(get_webdriver()))
