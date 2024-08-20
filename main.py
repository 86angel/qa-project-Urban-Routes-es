import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
import json
import time

# COMENTARIOS
# Hola Kevin, lamento tanta corrección pero ahora que estoy un poco más libre ya he podido realizar varias correcciones, entre ellas:
    # 1. Se cambiaron los selectores porque se eligieron los incorrectos, ahora ya se tienen selectores via XPATH
    # 2. Se agregaron validaciones nuevas que complementan a las anteriores
    # 3. Con chatGPT si hice cambios para poner el nombre de algunas variables en inglés porque al hacer las correcciones...las hice en español por descuido, así que, sinceramente aquí si tuve que facilitar las cosas

# No modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code

class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.CSS_SELECTOR, "button.button.round")
    comfort_rate_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')
    phone_button = (By.CLASS_NAME, "np-button")
    add_phone_number = (By.ID, 'phone')
    next_phone_button = (By.CSS_SELECTOR, ".button.full")
    enter_code_field = (By.ID, "code")
    confirm_code_button = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[2]/button[1]')
    payment_method_click = (By.CSS_SELECTOR, '.pp-button.filled')
    add_card_click = (By.CSS_SELECTOR, '.pp-row.disabled')
    fill_card_field = (By.ID, 'number')
    fill_pin_field = (By.XPATH, "//div[@class='card-code-input']//input[@id='code']")
    click_to_lose_focus = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[2]')
    add_card_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    close_popup_button = (By.CSS_SELECTOR, '#root > div > div.payment-picker.open > div.modal > div.section.active > button')
    get_payment_method = (By.CLASS_NAME, "pp-value-text")
    comment_field = (By.ID, "comment")
    blanket_and_tissues_slider = (By.CSS_SELECTOR, ".slider.round")
    add_ice_cream_button = (By.CLASS_NAME, 'counter-plus')
    get_ice_cream_count = (By.CLASS_NAME, 'counter-value')
    order_taxi = (By.CLASS_NAME, 'smart-button')
    popup_title = (By.CLASS_NAME, 'order-header-title')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        from_field_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.from_field))
        from_field_element.send_keys(from_address)

    def set_to(self, to_address):
        to_field_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.to_field))
        to_field_element.send_keys(to_address)

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def get_from(self):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.from_field)).get_property('value')

    def get_to(self):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.to_field)).get_property('value')

    def click_request_taxi_button(self):
        request = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.request_taxi_button))
        request.click()

    def click_comfort_button(self):
        comfort_click = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.comfort_rate_button))
        comfort_click.click()

    def get_comfort_button_text(self):
        comfort_text = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.comfort_rate_button)).text
        return comfort_text

    def click_phone_button(self):
        phone_click = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.phone_button))
        phone_click.click()

    def enter_phone_number(self, number):
        add_number = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.add_phone_number))
        add_number.send_keys(number)

    def click_next_phone_button(self):
        next_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.next_phone_button))
        next_button.click()

    def enter_code(self, code):
        enter_code = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.enter_code_field))
        enter_code.send_keys(code)

    def confirm_code(self):
        confirm_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.confirm_code_button))
        confirm_button.click()

    def get_phone_number(self):
        number = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.phone_button))
        return number.text

    def process_phone_number_entry(self, number):
        self.click_phone_button()
        self.enter_phone_number(number)
        self.click_next_phone_button()

    def process_phone_code(self, code):
        self.enter_code(code)
        self.confirm_code()

    def click_payment_method(self):
        credit_card = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.payment_method_click))
        credit_card.click()

    def click_add_card(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.add_card_click)).click()

    def process_payment_method_and_add_card(self):
        self.click_payment_method()
        self.click_add_card()

    def fill_card_number(self, card_number):
        enter_card = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.fill_card_field))
        enter_card.send_keys(card_number)

    def fill_pin(self, pin):
        enter_pin = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.fill_pin_field))
        enter_pin.send_keys(pin)

    def fill_card_and_pin(self, card_number, pin):
        self.fill_card_number(card_number)
        self.fill_pin(pin)

    def get_card_field_value(self):
        card_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.fill_card_field))
        return card_field.get_property('value')

    def get_pin_field_value(self):
        pin_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.fill_pin_field))
        return pin_field.get_property('value')

    def click_to_lose_focus(self):
        click_away = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.click_to_lose_focus))
        click_away.click()

    def click_add_card_button(self):
        add_card_click = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.add_card_button))
        add_card_click.click()

    def close_popup(self):
        close_window = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.close_popup_button))
        close_window.click()

    def process_lose_focus_add_card_close_popup(self):
        self.click_to_lose_focus()
        self.click_add_card_button()
        self.close_popup()

    def get_payment_method_text(self):
        payment_text = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.get_payment_method))
        return payment_text.text

    def add_comment_to_driver(self, message):
        add_comment = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.comment_field))
        add_comment.send_keys(message)

    def check_comment(self):
        check_comment = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.comment_field))
        return check_comment.get_attribute('value')

    def click_blanket_and_tissues(self):
        click_slider = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.blanket_and_tissues_slider))
        click_slider.click()

    def check_slider_selected(self):
        slider = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//div[@class='r-sw-container']/*[contains(text(),'Manta')]/..//div[@class='switch']//input[@class='switch-input']")))
        return slider.is_selected()

    def add_ice_cream(self):
        more_ice_cream = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.add_ice_cream_button))
        more_ice_cream.click()
        more_ice_cream.click()

    def get_ice_cream_count(self):
        ice_cream_count = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.get_ice_cream_count))
        return ice_cream_count.text

    def click_order_taxi(self):
        order = self.driver.find_element(self.order_taxi)
        order.click()

    def check_popup_present(self):
        popup = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(self.popup_title))
        return popup.text

    def wait_for_time(self):
        new_window = WebDriverWait(self.driver, 40).until(EC.text_to_be_present_in_element(self.popup_title, 'El conductor llegará en'))

    def check_driver_info(self):
        info = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located(self.popup_title))
        return info.text


class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        chrome_options = ChromeOptions()
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.maximize_window()
        cls.driver.delete_all_cookies()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_comfort_rate_text(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_request_taxi_button()
        routes_page.click_comfort_button()
        assert 'Comfort\n$10' == routes_page.get_comfort_button_text()

    def test_add_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        number = data.phone_number
        routes_page.process_phone_number_entry(number)
        code = retrieve_phone_code(self.driver)
        routes_page.process_phone_code(code)
        assert routes_page.get_phone_number() == number

    def test_add_credit_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.process_payment_method_and_add_card()
        card_number = data.card_number
        card_code = data.card_code
        routes_page.fill_card_and_pin(card_number, card_code)
        assert routes_page.get_card_field_value() == card_number
        assert routes_page.get_pin_field_value() == card_code
        routes_page.process_lose_focus_add_card_close_popup()
        assert routes_page.get_payment_method_text() == 'Tarjeta'

    def test_add_comment_to_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        comment = data.message_for_driver
        routes_page.add_comment_to_driver(comment)
        assert routes_page.check_comment() == comment

    def test_select_blanket_and_tissues(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_blanket_and_tissues()
        assert routes_page.check_slider_selected() == True

    def test_add_2_ice_creams(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.add_ice_cream()
        assert routes_page.get_ice_cream_count() == '2'

    def test_popup_presence(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_order_taxi()
        assert routes_page.check_popup_present() == 'Buscar automóvil'

    def test_optional_window(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.wait_for_time()
        assert 'El conductor llegará en' in routes_page.check_driver_info()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
