import ssl
import typing
import requests

class SSLAdapter(requests.adapters.HTTPAdapter):
    """
    Adaptador personalizado para la biblioteca requests que establece
    un contexto SSL más seguro para las peticiones HTTPS.
    
    Atributos:
        No hay atributos públicos.
    
    Métodos:
        init_poolmanager(*args, **kwargs): Inicializa el gestor de conexiones con
        un contexto SSL personalizado.
    
    Ejemplo:
        >>> session = requests.Session()
        >>> adapter = SSLAdapter()
        >>> session.mount('https://', adapter)
        >>> response = session.get('https://www.example.com')
        >>> print(response.status_code)
    """

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
        kwargs["ssl_context"] = context
        super().init_poolmanager(*args, **kwargs)
        