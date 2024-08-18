import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
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
    # Aquí prácticamente solo se agregan lo localizadores
    comfort_tariff_button = (By.CSS_SELECTOR, 'button.comfort-tariff')
    phone_field = (By.ID, 'phone')
    card_number_field = (By.ID, 'card_number')
    card_code_field = (By.ID, 'code')
    link_card_button = (By.ID, 'link_card')
    message_field = (By.ID, 'message_for_driver')
    blanket_checkbox = (By.ID, 'blanket_request')
    tissues_checkbox = (By.ID, 'tissues_request')
    ice_cream_quantity_field = (By.ID, 'ice_cream_quantity')
    search_driver_modal = (By.ID, 'search_driver_modal')
    driver_info = (By.CLASS_NAME, 'driver-info')


    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def select_comfort_tariff(self):
        self.driver.find_element(*self.comfort_tariff_button).click()

    def set_phone_number(self, phone_number):
        self.driver.find_element(*self.phone_field).send_keys(phone_number)

    def add_credit_card(self, card_number, card_code):
        self.driver.find_element(*self.card_number_field).send_keys(card_number)
        card_code_input = self.driver.find_element(*self.card_code_field)
        card_code_input.send_keys(card_code)
        card_code_input.send_keys(Keys.TAB)  # Cambiar el enfoque para activar el botón
        self.driver.find_element(*self.link_card_button).click()

    def write_message_for_driver(self, message):
        self.driver.find_element(*self.message_field).send_keys(message)

    def request_blanket_and_tissues(self):
        self.driver.find_element(*self.blanket_checkbox).click()
        self.driver.find_element(*self.tissues_checkbox).click()

    def request_ice_cream(self, quantity):
        ice_cream_field = self.driver.find_element(*self.ice_cream_quantity_field)
        ice_cream_field.clear()
        ice_cream_field.send_keys(quantity)

    def wait_for_driver_info(self):
        WebDriverWait(self.driver, 120).until(
            expected_conditions.visibility_of_element_located(self.driver_info)
        )

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # No lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_full_taxi_order(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # Configurar la dirección
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

        # Seleccionar la tarifa Comfort
        routes_page.select_comfort_tariff()

        # Rellenar el número de teléfono
        routes_page.set_phone_number(data.phone_number)

        # Agregar una tarjeta de crédito
        routes_page.add_credit_card(data.card_number, data.card_code)
        # Se puede usar la función retrieve_phone_code() aquí si es necesario

        # Escribir un mensaje para el conductor
        routes_page.write_message_for_driver(data.message_for_driver)

        # Pedir una manta y pañuelos
        routes_page.request_blanket_and_tissues()

        # Pedir 2 helados
        routes_page.request_ice_cream(2)

        # Esperar a que aparezca la información del conductor
        routes_page.wait_for_driver_info()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
