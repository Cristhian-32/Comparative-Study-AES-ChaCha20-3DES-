import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend

class ChaCha20:
    def __init__(self):
        self.backend = default_backend()

    def encrypt(self, plaintext: np.ndarray, key: np.ndarray, nonce: np.ndarray) -> np.ndarray:
        # Asegurar tamaños correctos
        key_bytes = bytes(key[:32])  # ChaCha20 usa clave de 256 bits
        nonce_bytes = bytes(nonce[:16])  # cryptography requiere 128 bits (16 bytes)

        if len(nonce_bytes) != 16:
            raise ValueError(f"Nonce inválido ({len(nonce_bytes)} bytes, se requieren 16)")

        cipher = Cipher(algorithms.ChaCha20(key_bytes, nonce_bytes), mode=None, backend=self.backend)
        encryptor = cipher.encryptor()

        ciphertext = encryptor.update(plaintext.tobytes()) + encryptor.finalize()
        return np.frombuffer(ciphertext, dtype=np.uint8)

    def decrypt(self, ciphertext: np.ndarray, key: np.ndarray, nonce: np.ndarray) -> np.ndarray:
        key_bytes = bytes(key[:32])
        nonce_bytes = bytes(nonce[:16])

        cipher = Cipher(algorithms.ChaCha20(key_bytes, nonce_bytes), mode=None, backend=self.backend)
        decryptor = cipher.decryptor()

        plaintext = decryptor.update(ciphertext.tobytes()) + decryptor.finalize()
        return np.frombuffer(plaintext, dtype=np.uint8)
