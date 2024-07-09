from typing import List
import importlib.util
import subprocess
import logging
import socket
import sys

class PackageManager:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def install(self, package: str) -> None:
        """Intenta instalar un paquete usando pip.
        
        Args:
            package (str): El nombre del paquete a instalar.
        
        Raises:
            RuntimeError: Si la instalación del paquete falla.
        """
        try:
            logging.info(f"Instalando paquete: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logging.info(f"Paquete instalado: {package}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error al instalar la librería {package}")
            raise RuntimeError(f"Error al instalar la librería {package}") from e

    def is_installed(self, package: str) -> bool:
        """Verifica si un paquete está instalado.
        
        Args:
            package (str): El nombre del paquete a verificar.
        
        Returns:
            bool: True si el paquete está instalado, False de lo contrario.
        """
        package_name = package.split('==')[0]  # Para manejar versiones específicas
        spec = importlib.util.find_spec(package_name)
        return spec is not None

    def ensure_installed(self, packages: List[str]) -> None:
        """Asegura que los paquetes dados estén instalados.
        
        Args:
            packages (List[str]): Una lista de nombres de paquetes a asegurar que estén instalados.
        
        Raises:
            RuntimeError: Si no hay conexión a Internet.
        """
        if not self._has_internet_connection():
            logging.error("No hay conexión a Internet. No se pueden instalar los paquetes.")
            raise RuntimeError("No hay conexión a Internet.")

        for package in packages:
            if not self.is_installed(package):
                self.install(package)

    def _has_internet_connection(self, timeout: int = 5) -> bool:
        """Verifica si hay una conexión a Internet disponible.
        
        Args:
            timeout (int): Tiempo de espera para la conexión en segundos. Predeterminado a 5 segundos.
        
        Returns:
            bool: True si hay conexión a Internet, False de lo contrario.
        """
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
            return True
        except socket.error:
            logging.error("Error de conexión a Internet")
            return False

if __name__ == "__main__":
    # Ejemplo de uso
    packages = ["requests", "numpy", "pandas"]
    installer = PackageManager()
    try:
        installer.ensure_installed(packages)
    except RuntimeError as e:
        print(e)
