import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class Camellia:
    def __init__(self):
        self.backend = default_backend()

    def encrypt(self, plaintext: np.ndarray, key: np.ndarray, iv: np.ndarray) -> np.ndarray:
        # --- Validación y preparación de datos ---
        # Camellia admite claves de 128, 192 o 256 bits
        if len(key) not in (16, 24, 32):
            raise ValueError(f"Longitud de clave inválida ({len(key)} bytes). Debe ser 16, 24 o 32 bytes (128/192/256 bits).")

        # IV de 16 bytes (128 bits) para modos como CBC
        if len(iv) != 16:
            raise ValueError(f"IV inválido ({len(iv)} bytes). Debe tener 16 bytes (128 bits).")

        key_bytes = bytes(key)
        iv_bytes = bytes(iv)

        # --- Configuración del cifrador ---
        cipher = Cipher(algorithms.Camellia(key_bytes), modes.CBC(iv_bytes), backend=self.backend)
        encryptor = cipher.encryptor()

        # --- Asegurar múltiplo del bloque (16 bytes) ---
        plaintext_bytes = plaintext.tobytes()
        padding_len = 16 - (len(plaintext_bytes) % 16)
        plaintext_bytes += bytes([padding_len]) * padding_len  # PKCS#7 simple

        # --- Cifrar ---
        ciphertext = encryptor.update(plaintext_bytes) + encryptor.finalize()
        return np.frombuffer(ciphertext, dtype=np.uint8)

    def decrypt(self, ciphertext: np.ndarray, key: np.ndarray, iv: np.ndarray) -> np.ndarray:
        # --- Validación y preparación ---
        if len(key) not in (16, 24, 32):
            raise ValueError(f"Longitud de clave inválida ({len(key)} bytes).")
        if len(iv) != 16:
            raise ValueError(f"IV inválido ({len(iv)} bytes).")

        key_bytes = bytes(key)
        iv_bytes = bytes(iv)

        cipher = Cipher(algorithms.Camellia(key_bytes), modes.CBC(iv_bytes), backend=self.backend)
        decryptor = cipher.decryptor()

        # --- Descifrar ---
        plaintext_padded = decryptor.update(ciphertext.tobytes()) + decryptor.finalize()

        # --- Quitar padding ---
        padding_len = plaintext_padded[-1]
        plaintext_bytes = plaintext_padded[:-padding_len]

        return np.frombuffer(plaintext_bytes, dtype=np.uint8)
