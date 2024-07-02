import ssl
import typing
import requests
from requests.adapters import HTTPAdapter

class SSLAdapter(HTTPAdapter):
    """
    Adaptador personalizado para la biblioteca requests que establece un contexto SSL
    más seguro para las solicitudes HTTPS e incluye una opción de depuración para detalles
    de SSL/TLS.

    Atributos:
        debug (bool): Si es True, imprime los detalles del contexto SSL.

    Métodos:
        __init__(self, *args: typing.Any, debug: bool = False, **kwargs: typing.Any) -> None:
            Inicializa el adaptador con la opción de depuración.
        
        init_poolmanager(self, *args: typing.Any, **kwargs: typing.Any) -> None:
            Inicializa el gestor de conexiones con un contexto SSL personalizado

    Ejemplo:
        >>> session = requests.Session()
        >>> adapter = SSLAdapter(debug=True)
        >>> session.mount('https://', adapter)
        >>> response = session.get('https://www.example.com')
        >>> print(response.status_code)
    """

    def __init__(self, *args: typing.Any, debug: bool = False, **kwargs: typing.Any) -> None:
        """
        Inicializa el adaptador con la opción de depuración.

        Args:
            *args: Argumentos posicionales para el método de la superclase.
            debug (bool): Si es True, se imprimen los detalles del contexto SSL.
            **kwargs: Argumentos de palabra clave para el método de la superclase.
        """
        self.debug = debug
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """
        Inicializa el gestor de conexiones con un contexto SSL personalizado.

        Args:
            *args: Argumentos posicionales para el método de la superclase.
            **kwargs: Argumentos de palabra clave para el método de la superclase.
        """
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        # Define un conjunto de cifrados modernos y seguros
        context.set_ciphers(":".join([
            "ECDHE-ECDSA-AES128-GCM-SHA256",
            "ECDHE-ECDSA-CHACHA20-POLY1305",
            "ECDHE-RSA-AES128-GCM-SHA256",
            "ECDHE-RSA-CHACHA20-POLY1305",
            "ECDHE+AES128",
            "RSA+AES128",
            "ECDHE+AES256",
            "RSA+AES256",
            "ECDHE+3DES",
            "RSA+3DES"
        ]))
        # Asegura que solo se utilicen TLS 1.2 o versiones superiores
        context.minimum_version = ssl.TLSVersion.TLSv1_2

        if self.debug:
            print("Información de Depuración SSL/TLS")
            print(f"Versión mínima de TLS: {context.minimum_version}")
            print(f"Cifrados habilitados: {context.get_ciphers()}")

        kwargs["ssl_context"] = context
        super().init_poolmanager(*args, **kwargs)
