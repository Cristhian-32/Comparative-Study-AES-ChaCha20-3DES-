from ChaCha20 import ChaCha20
import numpy as np, os

key = np.array([0x03020100,0x07060504,0x0b0a0908,0x0f0e0d0c,0x13121110,0x17161514,0x1b1a1918,0x1f1e1d1c], dtype=np.uint32)
nonce = np.array([0x00000000,0x4a000000,0x00000000,0x00000001], dtype=np.uint32)
plaintext = np.frombuffer(b"HolaMundo123456", dtype=np.uint8)

c = ChaCha20()
cipher = c.encrypt(plaintext, key, nonce)
plain = c.decrypt(cipher, key, nonce)

print("Cifrado:", cipher)
print("Descifrado:", bytes(plain))
