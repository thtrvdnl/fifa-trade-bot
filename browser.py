import utils
import email
import imaplib
from typing import Optional, Tuple

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebWorker:
    URL = "https://www.ea.com/fifa/ultimate-team/web-app/"

    def __init__(self, driver: webdriver.Chrome):
        self._actions = None
        self.__driver = driver

    def _set_url(self) -> None:
        self.__driver.get(self.URL)

    def _set_action(self) -> None:
        self._actions = ActionChains(self.__driver)

    def _check_element(self, timeout: int, element: Tuple[By, str]) -> None:
        # Проверка на наличие html элемента
        WebDriverWait(self.__driver, timeout).until_not(
            EC.invisibility_of_element(element)
        )

    def _add_sequence_actions(self, element: Tuple[By, str]) -> None:
        element = self.__driver.find_element(*element)
        self._actions.move_to_element(element)
        utils.time_sleep(2)
        self._actions.click(element)
        utils.time_sleep(2)

    def log_in(self) -> None:
        print("Logging in...")
        self._check_element(60, (By.CLASS_NAME, "ut-login-content"))
        utils.time_sleep(2)
        self._add_sequence_actions(
            (By.CSS_SELECTOR, ".ut-login .ut-login-content .btn-standard")
        )
        self._actions.perform()

    def _sign_in_ea_account(self) -> None:
        self.__driver.find_element_by_name("email").send_keys(utils.env.str("LOGIN"))
        utils.time_sleep(2)
        self.__driver.find_element_by_name("password").send_keys(
            utils.env.str("PASSWORD_EA")
        )
        utils.time_sleep(2)
        self.__driver.find_element_by_id("btnLogin").click()

    def _login_verification(self) -> None:
        utils.time_sleep(2)
        self.__driver.find_element_by_id("btnSendCode").click()

    def _security_code(self) -> None:
        code = utils.get_secure_code_by_mail()
        self.__driver.find_element_by_name("oneTimeCode").send_keys(code)
        utils.time_sleep(2)
        self.__driver.find_element_by_id("btnSubmit").click()

    def email_authorization(self) -> None:
        self._check_element(60, (By.ID, "email-login-panel"))
        utils.time_sleep(2)

        self._sign_in_ea_account()

        self._check_element(30, (By.ID, "btnSendCode"))
        utils.time_sleep(2)

        self._login_verification()

        self._check_element(30, (By.CLASS_NAME, "panel-content"))
        utils.time_sleep(30)

        self._security_code()
        utils.time_sleep(60)

    def _check_update_message_in_fifa(self):
        # TODO: Окно обновления фифы надо чтобы оно закрывалось если есть
        utils.time_sleep(5)
        try:
            print('_check_update_message_in_fifa')
            self.__driver.find_element_by_class_name("ut-livemessage-footer").click()
            utils.time_sleep(3)
            self.__driver.find_element_by_class_name("ut-livemessage-footer").click()
        except Exception as exp:
            print(exp)

    def _go_to_transfer_market(self) -> None:
        utils.time_sleep(2)
        self.__driver.find_element_by_class_name("icon-transfer").click()
        # self._add_sequence_actions((By.CLASS_NAME, "icon-transfer"))
        utils.time_sleep(2)

    def _go_to_search_player_in_transfer_market(self):
        # TODO: Ебучий action не видит элементов после проверки. Приходится тупым методом.
        self._check_element(100, (By.CLASS_NAME, "icon-transfer"))
        utils.time_sleep(3)

        self._go_to_transfer_market()
        # self._actions.perform()

        # self._check_element(30, (By.CLASS_NAME, "tileContent"))
        self.__driver.find_element_by_class_name("tileContent").click()
        # self._actions.perform()

        self._check_element(30, (By.CLASS_NAME, "ut-text-input-control"))
        utils.time_sleep(2)

    def accept_player(self, player: utils.Player):
        # TODO: Джанго будет кидать игрока, которого надо мониторить
        # надо состояние о мониторинге игрока

    def start(self) -> None:
        self._set_url()
        self._set_action()
        self.log_in()
        self.email_authorization()
        self._check_update_message_in_fifa()
        self._go_to_search_player_in_transfer_market()


if __name__ == "__main__":
    webdriver = utils.get_webdriver()
    bot = WebWorker(webdriver)
    bot.start()
