from urllib.parse import urlparse, parse_qs
import requests
import re
import logging
from typing import Optional

# Configuración básica del logging para mostrar información relevante y errores.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ReCaptchaSolver:
    """
    Clase diseñada para resolver ReCaptcha v3 automatizando el proceso de obtención del token de respuesta.

    Atributos:
        url (str): URL de la página que contiene el ReCaptcha v3 a resolver.
        session (requests.Session): Sesión HTTP utilizada para realizar las solicitudes web.
        BASE_URL (str): URL base para las solicitudes a la API de ReCaptcha.

    Métodos:
        get_token(): Retorna el token de respuesta de ReCaptcha v3 como una cadena de texto.
    """
    
    BASE_URL = 'https://www.google.com/recaptcha/api2/'

    def __init__(self, url: str) -> None:
        """
        Inicializa el objeto ReCaptchaSolver con la URL proporcionada.

        Args:
            url (str): La URL de la página web que contiene el ReCaptcha v3.
        """
        self.session = requests.Session()
        self.url = url
        # Construye las URLs para las solicitudes de 'reload' y 'anchor' basándose en la URL base.
        self.api_reload_url = f'{self.BASE_URL}reload?{self._parse_query(url, "reload")}'
        self.api_anchor_url = f'{self.BASE_URL}anchor?{self._parse_query(url, "anchor")}'
        # Configuración de los headers HTTP para simular una solicitud de navegador.
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "es-ES,es;q=0.9",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Referer": self.api_anchor_url
        }

    def _parse_query(self, url: str, purpose: str) -> str:
        """
        Analiza la URL proporcionada y extrae la cadena de consulta relevante.

        Args:
            url (str): La URL completa desde la que se extraerán los parámetros.
            purpose (str): El propósito de la extracción, como 'reload' o 'anchor'.

        Returns:
            str: La parte relevante de la cadena de consulta para el propósito especificado.
        """
        query_string = urlparse(url).query
        if purpose == "reload":
            # Retorna el segundo parámetro de la consulta para 'reload'.
            return query_string.split("&")[1]
        # Retorna la cadena de consulta completa para otros propósitos.
        return query_string

    def get_token(self) -> Optional[str]:
        """
        Obtiene el token de ReCaptcha v3 realizando solicitudes web necesarias.

        Returns:
            Optional[str]: El token de respuesta si es exitoso, None si falla.
        """
        try:
            # Realiza la solicitud inicial para obtener datos necesarios.
            response = self.session.get(self.api_anchor_url, headers={"Accept": "*/*"})
            logging.info(f'Response time: {response.elapsed.total_seconds()}s')

            # Prepara los datos para la solicitud de token basada en la respuesta inicial.
            data = {
                "v": self._parse_query_param('v'),
                "reason": "q",
                "c": self._extract_value(response.text, "recaptcha-token"),
                "k": self._parse_query_param('k'),
                "co": self._parse_query_param('co'),
                "size": self._parse_query_param('size'),
                "cb": self._parse_query_param('cb'),
                "hl": self._parse_query_param('hl')
            }

            # Realiza la solicitud para obtener el token de ReCaptcha.
            token_response = self.session.post(self.api_reload_url, headers=self.headers, data=data)
            # Extrae el token de la respuesta.
            token = "".join(re.findall("\[\"rresp\",\"(.*?)\"", token_response.text))
            return token
        except requests.RequestException as e:
            logging.error(f"Error al obtener el token: {e}")
            return None

    def _parse_query_param(self, param: str) -> str:
        """
        Extrae y retorna un parámetro específico de la cadena de consulta de la URL.

        Args:
            param (str): El nombre del parámetro a extraer.

        Returns:
            str: El valor del parámetro especificado.
        """
        return parse_qs(urlparse(self.url).query).get(param, [''])[0]

    def _extract_value(self, text: str, id_value: str) -> str:
        """
        Busca y extrae un valor específico de un texto HTML, basado en un patrón.

        Args:
            text (str): El texto HTML desde el cual extraer el valor.
            id_value (str): El ID asociado al valor que se busca.

        Returns:
            str: El valor extraído.
        """
        return "".join(re.findall(f'type="hidden" id="{id_value}" value="(.*?)"', text))

# if __name__ == "__main__":
#     URL = input("Ingresa la URL del recaptcha >>> ")
#     solver = ReCaptchaSolver(URL)
#     token = solver.get_token()
#     if token:
#         print(f"Bypass Result Recaptcha >>> \n{token}")
#     else:
#         print("No se pudo obtener el token.")