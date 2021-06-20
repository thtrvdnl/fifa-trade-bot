import utils
from typing import Optional

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebWorker:
    URL = "https://www.ea.com/fifa/ultimate-team/web-app/"

    def __init__(self, driver: Optional[webdriver.Chrome]):
        self._actions = None
        self.__driver = driver

    def _set_url(self) -> None:
        self.__driver.get(self.URL)

    def _set_action(self) -> None:
        self._actions = ActionChains(self.__driver)

    def _add_sequence_actions(self, element: Optional[str]) -> None:
        element = self.__driver.find_element_by_css_selector(element)
        self._actions.move_to_element(element)
        utils.time_sleep()
        self._actions.click(element)

    def log_in(self) -> None:
        # Проверка на наличие класса
        WebDriverWait(self.__driver, 60).until_not(
            EC.invisibility_of_element((By.CLASS_NAME, "ut-login-content"))
        )
        print("Logging in...")
        utils.time_sleep()
        self._add_sequence_actions(".ut-login .ut-login-content .btn-standard")
        utils.time_sleep()
        self._actions.perform()

    def start(self):
        self._set_url()
        self._set_action()
        self.log_in()


if __name__ == "__main__":
    webdriver = utils.get_webdriver()
    bot = WebWorker(webdriver)
    bot.start()
