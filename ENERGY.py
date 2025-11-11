import psutil
import threading
import time
import numpy as np
import os
from AES import *
from ChaCha20 import *
from TDES import *
from Camellia import *

# Variables globales para medir CPU
CPU = 0
measuring = False

def measure():
    """Thread que actualiza el uso máximo de CPU (%) durante la ejecución de la función."""
    global CPU, measuring
    while measuring:
        cpu_now = psutil.cpu_percent(interval=0.1)
        CPU = max(CPU, cpu_now)
        time.sleep(0.1)

def measure_cpu_during(func, *args):
    """Ejecuta func y mide CPU máximo y tiempo de ejecución."""
    global CPU, measuring
    CPU = 0
    measuring = True
    t = threading.Thread(target=measure)
    t.start()
    t0 = time.time()
    func(*args)
    t1 = time.time()
    measuring = False
    t.join()
    exec_time = t1 - t0
    return CPU, exec_time

# --- TDP estimado de CPU (Watts) ---
CPU_TDP = 15  # Ajusta según tu CPU

# --- Llaves y configuración ---
AES128 = np.array([0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,
                   0x08,0x09,0x0a,0x0b,0x0c,0x0d,0x0e,0x0f], dtype=np.uint8)
ChaCha = np.array([0x03020100, 0x07060504, 0x0b0a0908, 0x0f0e0d0c,
                   0x13121110, 0x17161514, 0x1b1a1918, 0x1f1e1d1c], dtype=np.uint32)
nonce = np.frombuffer(os.urandom(16), dtype=np.uint8)
TDES1 = np.array([0,1,0,0,1,1,0,0,0,1,1,1,0,1,0,1]*4, dtype=np.uint8)
TDES2 = np.array([1,0,1,0,0,1,1,0,1,1,0,1,0,1,0,1]*4, dtype=np.uint8)
TDES3 = np.array([0,0,1,1,0,1,0,1,1,0,0,0,1,1,0,1]*4, dtype=np.uint8)
Camellia_key = np.frombuffer(os.urandom(32), dtype=np.uint8)
Camellia_iv = np.frombuffer(os.urandom(16), dtype=np.uint8)

# Crear carpeta de resultados
if not os.path.exists('./Resultados'):
    os.makedirs('./Resultados')

# CSV de salida
out_file = open('./Resultados/ENERGY_results.csv', 'w', encoding='utf-8')
out_file.write('Archivo,Peso (KB),Algoritmo,Energia Encrypt (J),Energia Encrypt (J/byte),'
               'Energia Decrypt (J),Energia Decrypt (J/byte)\n')

for file in os.listdir('./Datos'):
    path = './Datos/' + file
    data = np.fromfile(path, dtype=np.uint8)
    size_kb = os.path.getsize(path) / 1024

    crypAES = AES()
    crypChaCha = ChaCha20()
    crypTDES = TDES()
    crypCamellia = Camellia()

    # --- AES ---
    cpu_enc, t_enc = measure_cpu_during(crypAES.encrypt, data, AES128)
    enc_data = crypAES.encrypt(data, AES128)
    cpu_dec, t_dec = measure_cpu_during(crypAES.decrypt, enc_data, AES128)
    dec_data = crypAES.decrypt(enc_data, AES128)

    energy_enc_J = CPU_TDP * (cpu_enc / 100) * t_enc
    energy_dec_J = CPU_TDP * (cpu_dec / 100) * t_dec
    energy_enc_byte = energy_enc_J / len(data)
    energy_dec_byte = energy_dec_J / len(data)

    out_file.write(f'{file},{size_kb:.2f},AES,{energy_enc_J:.4f},{energy_enc_byte:.8f},'
                   f'{energy_dec_J:.4f},{energy_dec_byte:.8f}\n')

    # --- 3DES ---
    bits = np.unpackbits(data)
    cpu_enc, t_enc = measure_cpu_during(crypTDES.encrypt, bits, TDES1, TDES2, TDES3)
    enc_bits = crypTDES.encrypt(bits, TDES1, TDES2, TDES3)
    cpu_dec, t_dec = measure_cpu_during(crypTDES.decrypt, enc_bits, TDES1, TDES2, TDES3)
    dec_bits = crypTDES.decrypt(enc_bits, TDES1, TDES2, TDES3)

    energy_enc_J = CPU_TDP * (cpu_enc / 100) * t_enc
    energy_dec_J = CPU_TDP * (cpu_dec / 100) * t_dec
    energy_enc_byte = energy_enc_J / len(data)
    energy_dec_byte = energy_dec_J / len(data)

    out_file.write(f'{file},{size_kb:.2f},3DES,{energy_enc_J:.4f},{energy_enc_byte:.8f},'
                   f'{energy_dec_J:.4f},{energy_dec_byte:.8f}\n')

    # --- ChaCha20 ---
    cpu_enc, t_enc = measure_cpu_during(crypChaCha.encrypt, data, ChaCha, nonce)
    enc_data = crypChaCha.encrypt(data, ChaCha, nonce)
    cpu_dec, t_dec = measure_cpu_during(crypChaCha.decrypt, enc_data, ChaCha, nonce)
    dec_data = crypChaCha.decrypt(enc_data, ChaCha, nonce)

    energy_enc_J = CPU_TDP * (cpu_enc / 100) * t_enc
    energy_dec_J = CPU_TDP * (cpu_dec / 100) * t_dec
    energy_enc_byte = energy_enc_J / len(data)
    energy_dec_byte = energy_dec_J / len(data)

    out_file.write(f'{file},{size_kb:.2f},ChaCha20,{energy_enc_J:.4f},{energy_enc_byte:.8f},'
                   f'{energy_dec_J:.4f},{energy_dec_byte:.8f}\n')

    # --- Camellia ---
    cpu_enc, t_enc = measure_cpu_during(crypCamellia.encrypt, data, Camellia_key, Camellia_iv)
    enc_data = crypCamellia.encrypt(data, Camellia_key, Camellia_iv)
    cpu_dec, t_dec = measure_cpu_during(crypCamellia.decrypt, enc_data, Camellia_key, Camellia_iv)
    dec_data = crypCamellia.decrypt(enc_data, Camellia_key, Camellia_iv)

    energy_enc_J = CPU_TDP * (cpu_enc / 100) * t_enc
    energy_dec_J = CPU_TDP * (cpu_dec / 100) * t_dec
    energy_enc_byte = energy_enc_J / len(data)
    energy_dec_byte = energy_dec_J / len(data)

    out_file.write(f'{file},{size_kb:.2f},Camellia,{energy_enc_J:.4f},{energy_enc_byte:.8f},'
                   f'{energy_dec_J:.4f},{energy_dec_byte:.8f}\n')

out_file.close()
print("✅ Medición de energía completa. Resultados guardados en './Resultados/ENERGY_results.csv'")
