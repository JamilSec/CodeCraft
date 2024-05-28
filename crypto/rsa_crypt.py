from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import json

class RSACrypt:
    def __init__(self, public_key_path_or_text=None, private_key_path_or_text=None):
        # Cargar clave pública si se proporciona
        self.public_key = self.load_key(public_key_path_or_text) if public_key_path_or_text else None
        self.public_cipher = PKCS1_OAEP.new(self.public_key) if self.public_key else None

        # Cargar clave privada si se proporciona
        self.private_key = self.load_key(private_key_path_or_text) if private_key_path_or_text else None
        self.private_cipher = PKCS1_OAEP.new(self.private_key) if self.private_key else None

        if not self.public_key and not self.private_key:
            raise ValueError("Debe proporcionar al menos una clave pública o privada.")

    def load_key(self, key_path_or_text):
        if key_path_or_text.endswith('.pem'):
            with open(key_path_or_text, 'r') as pem_file:
                key = pem_file.read()
        else:
            key = self.format_pem_key(key_path_or_text)
        return RSA.import_key(key)

    def format_pem_key(self, pem_key):
        pem_key = pem_key.replace(" ", "").replace("\n", "")
        if "BEGINPUBLICKEY" in pem_key:
            pem_key = pem_key.replace("-----BEGINPUBLICKEY-----", "-----BEGIN PUBLIC KEY-----\n")
            pem_key = pem_key.replace("-----ENDPUBLICKEY-----", "\n-----END PUBLIC KEY-----")
        elif "BEGINPRIVATEKEY" in pem_key:
            pem_key = pem_key.replace("-----BEGINPRIVATEKEY-----", "-----BEGIN PRIVATE KEY-----\n")
            pem_key = pem_key.replace("-----ENDPRIVATEKEY-----", "\n-----END PRIVATE KEY-----")
        return pem_key

    def get_modulus_exponent(self):
        if not self.public_key:
            raise ValueError("La clave pública no está cargada.")
        modulus = self.public_key.n
        exponent = self.public_key.e
        return modulus, exponent

    def encrypt_data(self, data):
        if not self.public_cipher:
            raise ValueError("La clave pública no está cargada, no se puede cifrar.")
        if isinstance(data, dict):
            data = json.dumps(data)
        data = data.encode('utf-8')
        encrypted_data = self.public_cipher.encrypt(data)
        encrypted_data = base64.b64encode(encrypted_data).decode('utf-8')
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        if not self.private_cipher:
            raise ValueError("La clave privada no está cargada, no se puede descifrar.")
        encrypted_data = base64.b64decode(encrypted_data)
        decrypted_data = self.private_cipher.decrypt(encrypted_data)
        return decrypted_data.decode('utf-8')


# EJEMPLO DE USO

# from crypto.rsa_crypt import RSACrypt

# # Crear instancia del cifrador RSA con las claves necesarias
# rsa_crypt = RSACrypt(public_key_path_or_text="-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0VEmZ1Jh/...", private_key_path_or_text="-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDg...")

# # Obtener el módulo y el exponente de la clave pública
# modulus, exponent = rsa_crypt.get_modulus_exponent()
# print(f"Modulus: {modulus}")
# print(f"Exponent: {exponent}")

# # Cifrar datos
# data_to_encrypt = {"score": 1000, "game_id": "1", "season_id": "2"}
# encrypted_data = rsa_crypt.encrypt_data(data_to_encrypt)
# print(f"Encrypted Data: {encrypted_data}")

# # Descifrar datos
# decrypted_data = rsa_crypt.decrypt_data(encrypted_data)
# print(f"Decrypted Data: {decrypted_data}")