import matplotlib.pyplot as plt
import numpy as np

# Ruta del archivo de resultados
ruta = "Resultados/T.txt"

# Tamaño del archivo (en bytes)
# ⚠️ Cambia esto si tus audios tienen otro tamaño
tamaño_archivo = 1 * 1024 * 1024  # 1 MB = 1,048,576 bytes

# Algoritmos esperados
algoritmos = ["AES128", "AES192", "AES256", "3DES", "ChaCha20"]
tiempo_enc = {alg: [] for alg in algoritmos}
tiempo_des = {alg: [] for alg in algoritmos}

# Leer archivo línea por línea
with open(ruta, "r") as f:
    for linea in f:
        partes = linea.strip().split()
        if len(partes) < 3:
            continue
        for alg in algoritmos:
            if alg in partes:
                i = partes.index(alg)
                tiempo_enc[alg].append(float(partes[i + 1]))
                tiempo_des[alg].append(float(partes[i + 2]))

# Calcular promedios en milisegundos y velocidades en MB/s
prom_enc = [np.mean(tiempo_enc[alg]) * 1000 for alg in algoritmos]
prom_des = [np.mean(tiempo_des[alg]) * 1000 for alg in algoritmos]

vel_enc = [tamaño_archivo / np.mean(tiempo_enc[alg]) / (1024 * 1024) for alg in algoritmos]
vel_des = [tamaño_archivo / np.mean(tiempo_des[alg]) / (1024 * 1024) for alg in algoritmos]

# --------- GRAFICO 1: Tiempo promedio (ms) ---------
x = np.arange(len(algoritmos))
width = 0.35
plt.figure(figsize=(9, 6))
plt.bar(x - width/2, prom_enc, width, label="Encriptación", color="steelblue")
plt.bar(x + width/2, prom_des, width, label="Desencriptación", color="orange")
plt.xticks(x, algoritmos)
plt.ylabel("Tiempo promedio (ms)")
plt.title("Comparación promedio de tiempos (ms)")
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# --------- GRAFICO 2: Velocidad promedio (MB/s) ---------
plt.figure(figsize=(9, 6))
plt.bar(x - width/2, vel_enc, width, label="Encriptación", color="green")
plt.bar(x + width/2, vel_des, width, label="Desencriptación", color="red")
plt.xticks(x, algoritmos)
plt.ylabel("Velocidad promedio (MB/s)")
plt.title("Comparación de velocidad de cifrado y descifrado (MB/s)")
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()
