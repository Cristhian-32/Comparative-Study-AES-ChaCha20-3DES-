import time
import numpy as np
import os
from AES import *
from ChaCha20 import *
from TDES import *
from Camellia import *

# Llaves y configuración
AES_keys = {
    "AES128": np.array([0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,
                        0x08,0x09,0x0a,0x0b,0x0c,0x0d,0x0e,0x0f], dtype=np.uint8),
    "AES192": np.array([0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,
                        0x08,0x09,0x0a,0x0b,0x0c,0x0d,0x0e,0x0f,
                        0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17], dtype=np.uint8),
    "AES256": np.array([0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,
                        0x08,0x09,0x0a,0x0b,0x0c,0x0d,0x0e,0x0f,
                        0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17,
                        0x18,0x19,0x1a,0x1b,0x1c,0x1d,0x1e,0x1f], dtype=np.uint8)
}

Camellia_keys = {
    "Camellia128": (np.frombuffer(os.urandom(16), dtype=np.uint8), np.frombuffer(os.urandom(16), dtype=np.uint8)),  # 128-bit key
    "Camellia192": (np.frombuffer(os.urandom(24), dtype=np.uint8), np.frombuffer(os.urandom(16), dtype=np.uint8)),  # 192-bit key
    "Camellia256": (np.frombuffer(os.urandom(32), dtype=np.uint8), np.frombuffer(os.urandom(16), dtype=np.uint8))   # 256-bit key
}

ChaCha = np.array([0x03020100, 0x07060504, 0x0b0a0908, 0x0f0e0d0c,
                   0x13121110, 0x17161514, 0x1b1a1918, 0x1f1e1d1c], dtype=np.uint32)
nonce = np.frombuffer(os.urandom(16), dtype=np.uint8)

TDES1 = np.array([0,1,0,0,1,1,0,0,0,1,1,1,0,1,0,1]*4, dtype=np.uint8)
TDES2 = np.array([1,0,1,0,0,1,1,0,1,1,0,1,0,1,0,1]*4, dtype=np.uint8)
TDES3 = np.array([0,0,1,1,0,1,0,1,1,0,0,0,1,1,0,1]*4, dtype=np.uint8)

# Carpeta de salida
if not os.path.exists('./Resultados'):
    os.makedirs('./Resultados')

out_file = open('./Resultados/TIME_SPEED_results.csv', 'w', encoding='utf-8')
out_file.write('Archivo,Tamaño (KB),Algoritmo,Tiempo Encrypt (s),Velocidad Encrypt (bytes/s),Tiempo Decrypt (s),Velocidad Decrypt (bytes/s)\n')

# Procesar archivos
for file in os.listdir('./Datos'):
    path = './Datos/' + file
    data = np.fromfile(path, dtype=np.uint8)
    size_bytes = os.path.getsize(path)
    size_kb = size_bytes / 1024

    crypAES = AES()
    crypChaCha = ChaCha20()
    crypTDES = TDES()
    crypCamellia = Camellia()

    # --- AES en 3 versiones ---
    for name, key in AES_keys.items():
        t1 = time.time()
        enc_data = crypAES.encrypt(data, key)
        t2 = time.time()
        enc_time = t2 - t1
        enc_speed = size_bytes / enc_time if enc_time > 0 else 0

        t1 = time.time()
        dec_data = crypAES.decrypt(enc_data, key)
        t2 = time.time()
        dec_time = t2 - t1
        dec_speed = size_bytes / dec_time if dec_time > 0 else 0

        out_file.write(f'{file},{size_kb:.2f},{name},{enc_time:.6f},{enc_speed:.2f},{dec_time:.6f},{dec_speed:.2f}\n')

    # --- 3DES ---
    bits = np.unpackbits(data)
    t1 = time.time()
    enc_bits = crypTDES.encrypt(bits, TDES1, TDES2, TDES3)
    t2 = time.time()
    enc_time = t2 - t1
    enc_speed = size_bytes / enc_time if enc_time > 0 else 0

    t1 = time.time()
    dec_bits = crypTDES.decrypt(enc_bits, TDES1, TDES2, TDES3)
    t2 = time.time()
    dec_time = t2 - t1
    dec_speed = size_bytes / dec_time if dec_time > 0 else 0

    out_file.write(f'{file},{size_kb:.2f},3DES,{enc_time:.6f},{enc_speed:.2f},{dec_time:.6f},{dec_speed:.2f}\n')

    # --- ChaCha20 ---
    t1 = time.time()
    enc_data = crypChaCha.encrypt(data, ChaCha, nonce)
    t2 = time.time()
    enc_time = t2 - t1
    enc_speed = size_bytes / enc_time if enc_time > 0 else 0

    t1 = time.time()
    dec_data = crypChaCha.decrypt(enc_data, ChaCha, nonce)
    t2 = time.time()
    dec_time = t2 - t1
    dec_speed = size_bytes / dec_time if dec_time > 0 else 0

    out_file.write(f'{file},{size_kb:.2f},ChaCha20,{enc_time:.6f},{enc_speed:.2f},{dec_time:.6f},{dec_speed:.2f}\n')

    # --- Camellia en 3 versiones ---
    for name, (key, iv) in Camellia_keys.items():
        t1 = time.time()
        enc_data = crypCamellia.encrypt(data, key, iv)
        t2 = time.time()
        enc_time = t2 - t1
        enc_speed = size_bytes / enc_time if enc_time > 0 else 0

        t1 = time.time()
        dec_data = crypCamellia.decrypt(enc_data, key, iv)
        t2 = time.time()
        dec_time = t2 - t1
        dec_speed = size_bytes / dec_time if dec_time > 0 else 0

        out_file.write(f'{file},{size_kb:.2f},{name},{enc_time:.6f},{enc_speed:.2f},{dec_time:.6f},{dec_speed:.2f}\n')

out_file.close()
print("Medición completa. Resultados guardados en './Resultados/TIME_SPEED_results.csv'")
