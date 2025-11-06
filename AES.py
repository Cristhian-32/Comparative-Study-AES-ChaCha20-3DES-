# AES.py
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

class AES:
    def __init__(self):
        self.backend = default_backend()

    def encrypt(self, plaintext: np.ndarray, key: np.ndarray) -> np.ndarray:
        """
        Cifra los datos usando AES (CBC) con padding PKCS7.
        plaintext: np.ndarray de bytes
        key: np.ndarray de tamaño 16, 24 o 32 bytes
        """
        # Convertir arrays numpy a bytes
        key_bytes = key.tobytes()
        data_bytes = plaintext.tobytes()

        # Generar IV de 16 bytes
        iv = os.urandom(16)

        # Aplicar padding PKCS7 (bloques de 128 bits)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data_bytes) + padder.finalize()

        # Crear cifrador AES en modo CBC
        cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # Guardar IV al inicio del ciphertext (para descifrado posterior)
        output = iv + ciphertext

        # Convertir a np.ndarray (uint8) para mantener compatibilidad con tu código principal
        return np.frombuffer(output, dtype=np.uint8)

    def decrypt(self, ciphertext: np.ndarray, key: np.ndarray) -> np.ndarray:
        """
        Descifra los datos usando AES (CBC) con padding PKCS7.
        ciphertext: np.ndarray (el IV está incluido al inicio)
        key: np.ndarray de tamaño 16, 24 o 32 bytes
        """
        key_bytes = key.tobytes()
        data_bytes = ciphertext.tobytes()

        # Extraer IV (primeros 16 bytes)
        iv = data_bytes[:16]
        data = data_bytes[16:]

        # Crear descifrador
        cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(data) + decryptor.finalize()

        # Remover padding
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        # Convertir a np.ndarray (uint8)
        return np.frombuffer(plaintext, dtype=np.uint8)
