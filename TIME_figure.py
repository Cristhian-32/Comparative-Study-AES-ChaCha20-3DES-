import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('./Resultados/TIME_SPEED_results.csv', encoding='latin1')
df.columns = df.columns.str.strip()

algos = df['Algoritmo'].unique()
x = np.arange(len(algos))
width = 0.35

times_encrypt = [df[df['Algoritmo']==algo]['Tiempo Encrypt (s)'].mean() for algo in algos]
times_decrypt = [df[df['Algoritmo']==algo]['Tiempo Decrypt (s)'].mean() for algo in algos]
speeds_encrypt = [df[df['Algoritmo']==algo]['Velocidad Encrypt (bytes/s)'].mean() for algo in algos]
speeds_decrypt = [df[df['Algoritmo']==algo]['Velocidad Decrypt (bytes/s)'].mean() for algo in algos]

fig, ax1 = plt.subplots(figsize=(12,6))

bars1 = ax1.bar(x - width/2, times_encrypt, width, color='skyblue', label='Tiempo Encrypt (s)')
bars2 = ax1.bar(x + width/2, times_decrypt, width, color='lightgreen', label='Tiempo Decrypt (s)')

ax1.set_xlabel('Algoritmo')
ax1.set_ylabel('Tiempo (s)')
ax1.set_xticks(x)
ax1.set_xticklabels(algos)
ax1.legend(loc='upper left')

ax2 = ax1.twinx()
ax2.plot(x, speeds_encrypt, color='orange', marker='o', linestyle='-', label='Velocidad Encrypt (bytes/s)')
ax2.plot(x, speeds_decrypt, color='red', marker='o', linestyle='-', label='Velocidad Decrypt (bytes/s)')
ax2.set_ylabel('Velocidad (bytes/s)')
ax2.legend(loc='upper right')

plt.title('Comparativa de Tiempo y Velocidad de Encriptación/Desencriptación')
fig.tight_layout()
plt.show()
