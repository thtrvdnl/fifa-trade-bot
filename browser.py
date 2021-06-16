import utils

from typing import Optional
from selenium import webdriver


class WebWorker:
    def __init__(self, driver: Optional[webdriver.Chrome]):
        self.__driver = driver



if __name__ == '__main__':
    print(utils)