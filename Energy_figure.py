import pandas as pd
import matplotlib.pyplot as plt

# --- Leer CSV ---
df = pd.read_csv('./Resultados/ENERGY_results.csv', encoding='latin1')
df.columns = df.columns.str.strip()

# --- Algoritmos y colores ---
algos = df['Algoritmo'].unique()
colors = ['blue', 'green', 'orange', 'red', 'purple', 'brown', 'cyan', 'magenta']

# --- Gráfico de ENCRIPTACIÓN ---
plt.figure(figsize=(12,6))
for i, algo in enumerate(algos):
    df_algo = df[df['Algoritmo']==algo]
    plt.plot(df_algo['Peso (KB)'], df_algo['Energia Encrypt (J)'],
             color=colors[i%len(colors)], marker='o', linestyle='-', label=algo)

plt.xlabel('Tamaño de archivo (KB)')
plt.ylabel('Energía Encrypt (J)')
plt.title('Consumo de Energía en Encriptación por Algoritmo')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# --- Gráfico de DESENCRIPTACIÓN ---
plt.figure(figsize=(12,6))
for i, algo in enumerate(algos):
    df_algo = df[df['Algoritmo']==algo]
    plt.plot(df_algo['Peso (KB)'], df_algo['Energia Decrypt (J)'],
             color=colors[i%len(colors)], marker='o', linestyle='-', label=algo)

plt.xlabel('Tamaño de archivo (KB)')
plt.ylabel('Energía Decrypt (J)')
plt.title('Consumo de Energía en Desencriptación por Algoritmo')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
