import utils
import email
import imaplib
from typing import Optional

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

    def _add_sequence_actions(self, element: str) -> None:
        element = self.__driver.find_element_by_css_selector(element)
        self._actions.move_to_element(element)
        utils.time_sleep(2)
        self._actions.click(element)

    def log_in(self) -> None:
        # Проверка на наличие класса
        WebDriverWait(self.__driver, 60).until_not(
            EC.invisibility_of_element((By.CLASS_NAME, "ut-login-content"))
        )
        print("Logging in...")
        utils.time_sleep(2)
        self._add_sequence_actions(".ut-login .ut-login-content .btn-standard")
        utils.time_sleep(2)
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
        self.__driver.find_element_by_id("btnSendCode").click()

    def _security_code(self) -> None:
        code = utils.get_secure_code_by_mail()
        self.__driver.find_element_by_name("oneTimeCode").send_keys(code)
        utils.time_sleep(2)
        self.__driver.find_element_by_id("btnSubmit").click()

    def email_authorization(self) -> None:
        WebDriverWait(self.__driver, 60).until_not(
            EC.invisibility_of_element((By.ID, "email-login-panel"))
        )
        utils.time_sleep(2)

        self._sign_in_ea_account()

        WebDriverWait(self.__driver, 30).until_not(
            EC.invisibility_of_element((By.ID, "btnSendCode"))
        )
        utils.time_sleep(2)

        self._login_verification()

        WebDriverWait(self.__driver, 30).until_not(
            EC.invisibility_of_element((By.CLASS_NAME, "panel-content"))
        )
        utils.time_sleep(2)

        self._security_code()

    def check_update_message_in_fifa(self):
        # TODO: Обход нормальный сделать
        try:
            live_message = self.__driver.find_element_by_class_name("ut-livemessage")
        except Exception as exp:
            print(exp)

    def start(self) -> None:
        self._set_url()
        self._set_action()
        self.log_in()
        self.email_authorization()


if __name__ == "__main__":
    webdriver = utils.get_webdriver()
    bot = WebWorker(webdriver)
    bot.start()
