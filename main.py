from AES import *
from ChaCha20 import *
from TDES import *

import numpy as np
import time
import psutil
import threading
import os

CPU = 0
C = 0
encrypting = True

#Funcion que guarda un dato en un archivo
def store(data, typ, sep):
	result = open('./Resultados/'+typ+'.txt', 'a')
	result.write(str(data)+sep)
	result.close()

#Funcion que mide el consumo de CPU
def measure():
	global CPU
	global encrypting
	while encrypting:
		CPU = max(CPU, psutil.cpu_percent())
		time.sleep(0.5)

#Declaracion de llaves para los algoritmos
AES128 = np.array([0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0a,0x0b,0x0c,0x0d,0x0e,0x0f], dtype=np.uint8)
AES192 = np.array([0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0a,0x0b,0x0c,0x0d,0x0e,0x0f,0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17], dtype=np.uint8)
AES256 = np.array([0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0a,0x0b,0x0c,0x0d,0x0e,0x0f,0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17,0x18,0x19,0x1a,0x1b,0x1c,0x1d,0x1e,0x1f], dtype=np.uint8)
TDES1  = np.array([0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,1,0,1,0,0,0,1,0,1,0,1,1,0,0,1,1,1,1,0,0,0,1,0,0,1,1,0,1,0,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1], dtype=np.uint8)
TDES2  = np.array([1,0,0,0,0,1,0,1,0,0,1,0,0,0,1,1,0,1,0,0,0,1,0,1,0,1,0,0,0,1,1,1,1,0,0,0,1,0,0,1,1,0,1,0,1,0,1,0,1,1,0,0,1,1,0,1,1,0,1,0,1,1,0,1], dtype=np.uint8)
TDES3  = np.array([0,0,1,1,0,1,0,1,0,0,1,0,0,0,0,1,0,1,0,0,0,1,0,1,0,1,1,0,0,1,0,1,1,0,0,0,1,0,0,1,1,0,1,0,1,0,1,1,0,1,0,0,1,0,0,1,1,1,1,0,1,0,1,1], dtype=np.uint8)
ChaCha = np.array([0x03020100, 0x07060504, 0x0b0a0908, 0x0f0e0d0c, 0x13121110, 0x17161514, 0x1b1a1918, 0x1f1e1d1c], dtype=np.uint32)
nonce = np.frombuffer(os.urandom(16), dtype=np.uint8)

#Crea la carpeta donde almacenara los resultados
if not os.path.exists('./Resultados'):
	os.makedirs('./Resultados')

#Pregunta si se medira el tiempo, CPU o energia
print('1. Tiempo')
print('2. CPU')
print('3. Energia')

x = input()

if x == '2':
	#Inicia el thread de medicion de CPU
	th = threading.Thread(target=measure)
	th.start()

#Lee todos los arvhivos de prueba de la carpeta datos
for file in os.listdir('./Datos'):
	path = './Datos/'+file
	if x == '1':
		store(file, 'T', ' ')
		#encripta con AES128
		txt = np.fromfile(path, dtype=np.uint8)
		cryp = AES()
		startTime = time.time()
		res = cryp.encrypt(txt, AES128)
		tim = time.time() - startTime
		store('AES128', 'T', ' ')
		store(tim, 'T', ' ')
		txt = res.astype(np.uint8)
		#desencripta con AES128
		startTime = time.time()
		res = cryp.decrypt(txt, AES128)
		tim = time.time() - startTime
		store(tim, 'T', ' ')
		#encripta con AES192
		txt = np.fromfile(path, dtype=np.uint8)
		startTime = time.time()
		res = cryp.encrypt(txt, AES192)
		tim = time.time() - startTime
		store('AES192', 'T', ' ')
		store(tim, 'T', ' ')
		txt = res.astype(np.uint8)
		#desencripta con AES192
		startTime = time.time()
		res = cryp.decrypt(txt, AES192)
		tim = time.time() - startTime
		store(tim, 'T', ' ')
		#encripta con AES256
		txt = np.fromfile(path, dtype=np.uint8)
		startTime = time.time()
		res = cryp.encrypt(txt, AES256)
		tim = time.time() - startTime
		store('AES256', 'T', ' ')
		store(tim, 'T', ' ')
		txt = res.astype(np.uint8)
		#desencripta con AES256
		startTime = time.time()
		res = cryp.decrypt(txt, AES256)
		tim = time.time() - startTime
		store(tim, 'T', ' ')
		#encripta con 3DES
		txt = np.fromfile(path, dtype=np.uint8)
		txt = np.unpackbits(txt)
		cryp = TDES()
		startTime = time.time()
		res = cryp.encrypt(txt, TDES1, TDES2, TDES3)
		tim = time.time() - startTime
		store('3DES', 'T', ' ')
		store(tim, 'T', ' ')
		txt = res.astype(np.uint8)
		#desencripta con 3DES
		startTime = time.time()
		res = cryp.decrypt(txt, TDES1, TDES2, TDES3)
		tim = time.time() - startTime
		store(tim, 'T', ' ')
		#encripta con ChaCha20
		txt = np.fromfile(path, dtype=np.uint8)
		cryp = ChaCha20()
		startTime = time.time()
		res = cryp.encrypt(txt, ChaCha, nonce)
		tim = time.time() - startTime
		store('ChaCha20', 'T', ' ')
		store(tim, 'T', ' ')
		txt = res.astype(np.uint8)
		#desencripta con ChaCha20
		startTime = time.time()
		res = cryp.decrypt(txt, ChaCha, nonce)
		tim = time.time() - startTime
		store(tim, 'T', '\n')
	elif x == '2':
		store(file, 'C', ' ')
		#encripta con AES128
		txt = np.fromfile(path, dtype=np.uint8)
		cryp = AES()
		CPU = 0
		res = cryp.encrypt(txt, AES128)
		C = CPU
		store('AES128', 'C', ' ')
		store(C, 'C', ' ')
		txt = res.astype(np.uint8)
		#desencripta con AES128
		CPU = 0
		res = cryp.decrypt(txt, AES128)
		C = CPU
		store(C, 'C', ' ')
		#encripta con AES192
		txt = np.fromfile(path, dtype=np.uint8)
		CPU = 0
		res = cryp.encrypt(txt, AES192)
		C = CPU
		store('AES192', 'C', ' ')
		store(C, 'C', ' ')
		txt = res.astype(np.uint8)
		#desencripta con AES192
		CPU = 0
		res = cryp.decrypt(txt, AES192)
		C = CPU
		store(C, 'C', ' ')
		#encripta con AES256
		txt = np.fromfile(path, dtype=np.uint8)
		CPU = 0
		res = cryp.encrypt(txt, AES256)
		C = CPU
		store('AES256', 'C', ' ')
		store(C, 'C', ' ')
		txt = res.astype(np.uint8)
		#desencripta con AES256
		CPU = 0
		res = cryp.decrypt(txt, AES256)
		C = CPU
		store(C, 'C', ' ')
		#encripta con 3DES
		txt = np.fromfile(path, dtype=np.uint8)
		txt = np.unpackbits(txt)
		cryp = TDES()
		CPU = 0
		res = cryp.encrypt(txt, TDES1, TDES2, TDES3)
		C = CPU
		store('3DES', 'C', ' ')
		store(C, 'C', ' ')
		txt = res.astype(np.uint8)
		#desencripta con 3DES
		CPU = 0
		res = cryp.decrypt(txt, TDES1, TDES2, TDES3)
		C = CPU
		store(C, 'C', ' ')
		#encripta con ChaCha20
		txt = np.fromfile(path, dtype=np.uint8)
		cryp = ChaCha20()
		CPU = 0
		res = cryp.encrypt(txt, ChaCha, nonce)
		C = CPU
		store('ChaCha20', 'C', ' ')
		store(C, 'C', ' ')
		txt = res.astype(np.uint8)
		#desencripta con ChaCha20
		CPU = 0
		res = cryp.decrypt(txt, ChaCha, nonce)
		C = CPU
		store(C, 'C', '\n')
	else:
		store(file, 'E', ' ')
		#encripta con AES128
		txt = np.fromfile(path, dtype=np.uint8)
		cryp = AES()
		print('.')
		E = input()
		res = cryp.encrypt(txt, AES128)
		print('\007')
		print('Res')
		E = input()
		store('AES128', 'E', ' ')
		store(E, 'E', ' ')
		txt = res.astype(np.uint8)
		#desencripta con AES128
		print('.')
		E = input()
		res = cryp.decrypt(txt, AES128)
		print('\007')
		print('Res')
		E = input()
		store(E, 'E', ' ')
		#encripta con AES192
		txt = np.fromfile(path, dtype=np.uint8)
		print('.')
		E = input()
		res = cryp.encrypt(txt, AES192)
		print('\007')
		print('Res')
		E = input()
		store('AES192', 'E', ' ')
		store(E, 'E', ' ')
		txt = res.astype(np.uint8)
		#desencripta con AES192
		print('.')
		E = input()
		res = cryp.decrypt(txt, AES192)
		print('\007')
		print('Res')
		E = input()
		store(E, 'E', ' ')
		#encripta con AES256
		txt = np.fromfile(path, dtype=np.uint8)
		print('.')
		E = input()
		res = cryp.encrypt(txt, AES256)
		print('\007')
		print('Res')
		E = input()
		store('AES256', 'E', ' ')
		store(E, 'E', ' ')
		txt = res.astype(np.uint8)
		#desencripta con AES256
		print('.')
		E = input()
		res = cryp.decrypt(txt, AES256)
		print('\007')
		print('Res')
		E = input()
		store(E, 'E', ' ')
		#encripta con 3DES
		txt = np.fromfile(path, dtype=np.uint8)
		txt = np.unpackbits(txt)
		cryp = TDES()
		print('.')
		E = input()
		res = cryp.encrypt(txt, TDES1, TDES2, TDES3)
		print('\007')
		print('Res')
		E = input()
		store('3DES', 'E', ' ')
		store(E, 'E', ' ')
		txt = res.astype(np.uint8)
		#desencripta con 3DES
		print('.')
		E = input()
		res = cryp.decrypt(txt, TDES1, TDES2, TDES3)
		print('\007')
		print('Res')
		E = input()
		store(E, 'E', ' ')
		#encripta con ChaCha20
		txt = np.fromfile(path, dtype=np.uint8)
		cryp = ChaCha20()
		print('.')
		E = input()
		res = cryp.encrypt(txt, ChaCha, nonce)
		print('\007')
		print('Res')
		E = input()
		store('ChaCha20', 'E', ' ')
		store(E, 'E', ' ')
		txt = res.astype(np.uint8)
		#desencripta con ChaCha20
		print('.')
		E = input()
		res = cryp.decrypt(txt, ChaCha, nonce)
		print('\007')
		print('Res')
		E = input()
		store(E, 'E', '\n')

if x == '2':
	#Finaliza el thread de medicion de CPU
	encrypting = False