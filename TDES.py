# TDES.py
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class TDES:
    def __init__(self):
        self.backend = default_backend()

    def encrypt(self, plaintext: np.ndarray, key1: np.ndarray, key2: np.ndarray, key3: np.ndarray) -> np.ndarray:
        # Convertir a bytes y tomar los primeros 8 de cada uno
        key = key1.tobytes()[:8] + key2.tobytes()[:8] + key3.tobytes()[:8]

        if len(key) not in (16, 24):
            raise ValueError(f"Clave inválida: se esperaban 16 o 24 bytes, se obtuvo {len(key)} bytes")

        # Rellenar con ceros si no es múltiplo de 8 bytes
        padding_len = 8 - (len(plaintext) % 8)
        padded = plaintext.tobytes() + bytes([0] * padding_len)

        cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded) + encryptor.finalize()

        return np.frombuffer(ciphertext, dtype=np.uint8)

    def decrypt(self, ciphertext: np.ndarray, key1: np.ndarray, key2: np.ndarray, key3: np.ndarray) -> np.ndarray:
        key = key1.tobytes()[:8] + key2.tobytes()[:8] + key3.tobytes()[:8]

        cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=self.backend)
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext.tobytes()) + decryptor.finalize()

        return np.frombuffer(plaintext, dtype=np.uint8)
