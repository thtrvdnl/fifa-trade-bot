import re
import time

import utils
import email
import imaplib
from typing import Optional, Tuple, Union

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebWorker:
    URL = "https://www.ea.com/fifa/ultimate-team/web-app/"

    def __init__(self, driver: webdriver.Chrome) -> None:
        self.player_parameters = {}

        self._actions = None
        self.__driver = driver
        print('WebWorker')

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

    @utils.print_func
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
        self.__driver.find_element_by_id("logInBtn").click()

    def _login_verification(self) -> None:
        utils.time_sleep(2)
        self.__driver.find_element_by_id("btnSendCode").click()

    def _security_code(self) -> None:
        code = utils.get_secure_code_by_mail()
        self.__driver.find_element_by_name("oneTimeCode").send_keys(code)
        utils.time_sleep(2)
        self.__driver.find_element_by_id("btnSubmit").click()

    @utils.print_func
    def email_authorization(self) -> None:
        self._check_element(60, (By.ID, "login-with-OriginId-or-Email-panel"))
        utils.time_sleep(2)
        print("_sign_in_ea_account")
        self._sign_in_ea_account()
        print("_sign_in_ea_account")
        print("btnSendCode")
        try:
            self._check_element(30, (By.ID, "btnSendCode"))
        except TimeoutException:
            return
        utils.time_sleep(2)
        print("btnSendCode")
        print("_login_verification")
        self._login_verification()
        print("_login_verification")
        print("views")
        self._check_element(30, (By.CLASS_NAME, "views"))
        utils.time_sleep(15)
        print("views")
        print("_security_code")
        self._security_code()
        utils.time_sleep(15)
        print("_security_code")

    @utils.print_func
    def _check_update_message_in_fifa(self) -> None:
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
        utils.time_sleep(2)

    @utils.print_func
    def _go_to_search_player_in_transfer_market(self) -> None:
        # TODO: Ебучий action не видит элементов после проверки. Приходится тупым методом.
        self._check_element(100, (By.CLASS_NAME, "icon-transfer"))
        utils.time_sleep(3)

        self._go_to_transfer_market()

        self._check_element(30, (By.CLASS_NAME, "tileContent"))
        self.__driver.find_element_by_class_name("tileContent").click()

        self._check_element(30, (By.CLASS_NAME, "ut-text-input-control"))
        utils.time_sleep(2)

    def accept_player(self, player: utils.Player):
        # TODO: Джанго будет кидать игрока, которого надо мониторить
        # надо состояние о мониторинге игрока
        pass

    def _get_all_player_parameters(self, tag_html: str) -> list:
        player_params_html = (By.CLASS_NAME, tag_html)
        self._check_element(30, player_params_html)

        player_params_element = self.__driver.find_element(*player_params_html)
        html_params = player_params_element.get_attribute('innerHTML')
        print(player_params_element)

        player_params = [param.split('</span>')[0] for param in html_params.split('<span class="label">')][1:]
        print('player_params %s' % player_params)

        return player_params

    # def _get_player_buy_fields(self) -> list:
    #     player_buy_fields_html = (By.CLASS_NAME, "search-prices")
    #     self._check_element(10, player_buy_fields_html)
    #
    #     player_buy_fields_element = self.__driver.find_element(*player_buy_fields_html)
    #
    #     html_params = player_params_element.get_attribute('innerHTML')

    def _find_element_in_transfer_market(self, element: str, many: bool = False) -> str:
        print("element", element)
        self._check_element(10, (By.XPATH, f"//{element}"))
        if many:
            element = self.__driver.find_elements_by_xpath(f"//{element}")
        else:
            element = self.__driver.find_element_by_xpath(f"//{element}")
        return element

    @staticmethod
    def check_param_in_player_msg(player: utils.Player, param: str) -> str:
        # processing parameter in particular "Chemistry Style" -> "chemistry_style"
        attr = getattr(player, param.lower() if not param.find(' ') else param.lower().replace(' ', '_'))
        attr = attr.split('=')[-1]
        return attr if attr != "''" else False

    @staticmethod
    def _send_player_buy_fields(player: utils.Player, buy_fields: str) -> None:
        # tuple = (min_price, max_price)
        bid_price: tuple[Union[int, str], Union[int, str]] = player.get_prices('bid_price')
        bid_now_price: tuple[Union[int, str], Union[int, str]] = player.get_prices('buy_now_price')
        for field, price in zip(buy_fields, (bid_price + bid_now_price)):
            utils.time_sleep(2)
            field.send_keys(price)

    def _click_transfer_button(self, text: str) -> None:
        self._find_element_in_transfer_market(f"button[text()='{text}']").click()

    @utils.print_func
    def find_player(self, player: utils.Player) -> None:
        player_params = self._get_all_player_parameters("ut-item-search-view")
        player_name = self._find_element_in_transfer_market("input[@placeholder='Type Player Name']")
        player_buy_fields = self._find_element_in_transfer_market("input[@placeholder='Any']", many=True)

        player_name.send_keys(player.name)
        self._find_element_in_transfer_market(f"span[text()='{player.name}']").click()

        for param in player_params:
            check_param = self.check_param_in_player_msg(player, param)
            check_param = utils.situations_have_changed(param, check_param)
            print("check_param", check_param)
            if check_param:
                utils.time_sleep(3)
                element_param = self._find_element_in_transfer_market(f"span[text()='{param}']")
                element_param.click()
                utils.time_sleep(2)
                element_inline_list = self._find_element_in_transfer_market(f"li[text()='{check_param}']")
                element_inline_list.click()
                utils.time_sleep(3)

        self._send_player_buy_fields(player, player_buy_fields)

        self._click_transfer_button("Search")

    @utils.print_func
    def _search_no_results(self) -> bool:
        time_ = time.time()
        try:
            self._check_element(1, (By.CLASS_NAME, "entityContainer"))
            return False
        except TimeoutException:
            print(f"TimeoutException {time.time()-time_}")
            return True

    def _come_back(self) -> None:
        #utils.time_sleep(1)
        self.__driver.find_element_by_class_name("ut-navigation-button-control").click()
        #utils.time_sleep(1)

    def _change_price(self, delta_price: int) -> None:
        bid_now_price_min: int = delta_price
        bid_price_min = self._find_element_in_transfer_market("input[@placeholder='Any']", many=True)[0]
        old_bid_price_min = int(bid_price_min.get_attribute("value"))
        if old_bid_price_min == delta_price:
            bid_now_price_min += 50

        utils.time_sleep(2)
        bid_price_min.send_keys(Keys.DELETE)
        time.sleep(1)
        print("bid_now_price_min", bid_now_price_min)
        bid_price_min.send_keys(bid_now_price_min)
        self._click_transfer_button("Search")

    def _search_notification_negative(self) -> bool:
        try:
            self._check_element(5, (By.CLASS_NAME, "Notification negative"))
            return True
        except TimeoutException:
            return False

    def _search_successful_buy(self) -> bool:
        try:
            self._check_element(5, (By.CLASS_NAME, "listFUTItem has-auction-data selected won"))
            return True
        except TimeoutException:
            return False

    @utils.print_func
    def _buy_players(self, count_buy_player: int, delta_price: int, player_numbers: str) -> None:
        time1 = time.time()
        li_list_players = self.__driver.find_elements_by_class_name("entityContainer")
        print("li_list_players", li_list_players)
        player = li_list_players[0]
        time2 = time.time()
        print(player)
        player.click()

        self._check_element(30, (By.CSS_SELECTOR, "button.btn-standard.buyButton.currency-coins"))
        button_buy_player_now = self.__driver.find_element_by_css_selector(
            "button.btn-standard.buyButton.currency-coins")
        print("button_list_players", button_buy_player_now)
        button_buy_player_now.click()
        print(f"===BUY TIME=== time1:{time.time()-time1} time2{time.time()-time2}")

        self._check_element(10, (By.XPATH, "//span[text()='Ok']"))
        element_button_ok = self._find_element_in_transfer_market("span[text()='Ok']")
        element_button_ok.click()

        button_send_to_transfer_list = self._find_element_in_transfer_market("span[text()='Send to Transfer List']")
        button_send_to_transfer_list.click()

        print("count_buy_player", count_buy_player)

    @utils.print_func
    def buy_players(self, player: utils.Player) -> str:
        count_buy_player = 0
        # нужно для обновления игроков
        delta_price = 150
        self.find_player(player)
        while count_buy_player < int(player.numbers):
            print("count_buy_player while", count_buy_player)
            print("find_player")
            time_ = time.time()
            if self._search_no_results():
                print("_search_no_results True")
                self._come_back()
                self._change_price(delta_price)
            else:
                print(f"buy_players:else {time.time()-time_}")
                self._buy_players(count_buy_player, delta_price, player.numbers)
                print("buy_players:else1")
                self._come_back()
                self._change_price(delta_price)
        self._click_transfer_button("Reset")
        return "Done"

    @utils.print_func
    def start(self) -> str:
        self._set_url()
        self._set_action()
        self.log_in()
        self.email_authorization()
        self._check_update_message_in_fifa()
        self._go_to_search_player_in_transfer_market()
        return "Status browser - activated"


if __name__ == "__main__":
    webdriver = utils.get_webdriver()
    bot = WebWorker(webdriver)
    bot.start(utils.Player("Bacy", "1", "2", "3", "4", "5", "6", "7"))
