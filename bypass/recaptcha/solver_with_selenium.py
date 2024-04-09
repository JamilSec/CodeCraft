from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import logging

# Configuración básica del logging para mostrar mensajes de información y errores.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL que contiene el reCAPTCHA v2 a ser resuelto.
URL_WITH_RECAPTCHA = 'https://example.com'

# Clave de sitio web para reCAPTCHA v2; debe ser proporcionada por el desarrollador.
API_KEY_WEB_SITE = '...'

class WebDriverFactory:
    """
    Fábrica para crear instancias de WebDriver basadas en el navegador especificado.
    """

    @staticmethod
    def create_driver(browser_name="firefox"):
        """
        Crea y retorna una instancia de WebDriver para el navegador especificado.
        
        Args:
            browser_name (str): El nombre del navegador para el cual crear el WebDriver.
                                Actualmente solo soporta "firefox".
        
        Returns:
            WebDriver: Una instancia del WebDriver para el navegador especificado.
        
        Raises:
            ValueError: Si el navegador especificado no es soportado.
        """
        if browser_name.lower() == "firefox":
            options = Options()
            # Configuraciones para un funcionamiento óptimo y sin GUI del navegador Firefox.
            options.add_argument("--headless")
            options.add_argument('--no-sandbox')
            options.add_argument("--incognito")
            options.add_argument('--disable-gpu')
            options.add_argument("--disable-extensions")
            return webdriver.Firefox(options=options)
        # Se puede extender para soportar otros navegadores si se desea.
        raise ValueError(f"Browser '{browser_name}' no es soportado.")

class BypassRecaptchaV2Selenium:
    """
    Clase diseñada para interactuar con páginas web que utilizan reCAPTCHA v2,
    obteniendo un token de reCAPTCHA mediante la inyección de JavaScript.
    """

    def __init__(self, driver):
        """
        Inicializa la instancia con el WebDriver proporcionado.
        
        Args:
            driver (WebDriver): Una instancia de WebDriver usada para controlar el navegador.
        """
        self.driver = driver

    def get_token(self):
        """
        Navega a la URL especificada que contiene un reCAPTCHA v2 y obtiene el token de reCAPTCHA.
        
        Returns:
            str: El token de reCAPTCHA obtenido mediante la inyección de JavaScript.
        """
        try:
            logging.info('Abriendo navegador...')
            self.driver.get(URL_WITH_RECAPTCHA)
            # Espera hasta que el elemento especificado esté presente en la página.
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.ID, "holder-calendar")))
            logging.info('Inyectando JS')
            # Script de JavaScript para ejecutar el reCAPTCHA y obtener el token.
            token_script = f"return grecaptcha.execute('{API_KEY_WEB_SITE}', {{action: 'submit'}}).then(function(token) {{return token;}});"
            token = self.driver.execute_script(token_script)
            return token
        except Exception as e:
            logging.error(f"Error obteniendo token: {e}")
        finally:
            # Asegura que el navegador se cierre después de la operación.
            self.close()

    def close(self):
        """
        Cierra el navegador manejado por este WebDriver.
        """
        logging.info('Cerrando navegador...')
        self.driver.quit()

# Ejemplo de cómo se usaría esta clase si se descomenta.
# if __name__ == "__main__":
#     driver = WebDriverFactory.create_driver("firefox")
#     scraper = BypassRecaptchaV2Selenium(driver)
#     token = scraper.get_token()
#     if token:
#         logging.info(f"Token reCAPTCHA: {token}")
#     else:
#         logging.error("No se pudo obtener el token.")
