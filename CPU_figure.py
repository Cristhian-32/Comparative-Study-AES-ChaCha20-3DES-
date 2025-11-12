import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./Resultados/CPU_results.csv')

plt.figure(figsize=(10,6))
for algo in df['Algoritmo'].unique():
    subset = df[df['Algoritmo'] == algo]
    plt.plot(subset['Peso (KB)'], subset['CPU Encrypt (%)'], label=algo)

plt.xlabel('Peso del archivo (KB)')
plt.ylabel('Uso máximo de CPU (%)')
plt.title('Consumo de CPU en Encriptación por Algoritmo')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,6))
for algo in df['Algoritmo'].unique():
    subset = df[df['Algoritmo'] == algo]
    plt.plot(subset['Peso (KB)'], subset['CPU Decrypt (%)'], label=algo)

plt.xlabel('Peso del archivo (KB)')
plt.ylabel('Uso máximo de CPU (%)')
plt.title('Consumo de CPU en Desencriptación por Algoritmo')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
