"""  (punto 1,2 y 3)
Parámetro			        MP3 original		WAV convertido
Formato				        MPEG Audio (MP3)	Wave (PCM)
Tasa de bits			    256 kb/s		    256 kb/s
Canales				        1 (mono)		    1 (mono)
Frecuencia de muestreo		48.000 Hz		    16.000 Hz
"""


import soundfile as sf
import matplotlib.pyplot as plt
import pygame
import time

# === PUNTO 4 – Cargar el audio y mostrar datos ===
audio, sr = sf.read("C:/Users/QueresUnMate/Desktop/G/AnalisisTextos.wav")

print("🔹 Vector de la señal (primeros valores):")
print(audio[:20])  # Mostramos solo los primeros para no saturar

print("🔹 Largo del array:", len(audio))
print("🔹 Frecuencia de muestreo:", sr)
print("🔹 Duración (s):", len(audio) / sr)

# === PUNTO 5 – Graficar la señal sonora ===
plt.figure(figsize=(10, 4))
plt.plot(audio)
plt.title("Señal de Audio")
plt.xlabel("Muestra")
plt.ylabel("Amplitud")
plt.grid(True)
plt.tight_layout()
plt.show()

# === PUNTO 6 – Reproducir el audio ===
print("🔈 Reproduciendo señal original...")
pygame.mixer.init(frequency=sr)
pygame.mixer.music.load("C:/Users/QueresUnMate/Desktop/G/AnalisisTextos.wav")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    time.sleep(0.1)
print("✅ Reproducción finalizada.")

import sounddevice as sd

# === PUNTO 7 – Reproducir el audio a distinta frecuencia ===

print("🎧 Reproduciendo audio original (frecuencia normal):")
sd.play(audio, sr)
sd.wait()

print("🎧 Reproduciendo audio acelerado (frecuencia x2):")
sd.play(audio, sr * 2)
sd.wait()

print("🎧 Reproduciendo audio más lento (frecuencia /2):")
sd.play(audio, sr // 2)
sd.wait()

"""punto 7
Probamos cómo cambia el sonido al reproducirlo con el doble o la mitad de la frecuencia original.
Al subirla, el audio se escucha más rápido y agudo; al bajarla, más lento y grave.
Esto no modifica el archivo, solo cómo se interpreta su velocidad de reproducción.
"""

import numpy as np

# === Punto 8 – Simular calidad de 8 bits ===

# Escalamos y convertimos a int8 (8 bits)
audio_8bits = (audio * (2**7 - 1)).astype(np.int8)

# Lo volvemos a escalar para reproducir como float (-1 a 1)
audio_8bits_norm = audio_8bits.astype(np.float32) / (2**7 - 1)

print("🎧 Reproduciendo audio con calidad simulada de 8 bits...")
sd.play(audio_8bits_norm, sr)
sd.wait()

"""punto 8
Simulamos bajar la calidad del audio a 8 bits.
Esto reduce la cantidad de niveles para representar el sonido,
haciendo que se escuche más áspero o con menos detalle.
"""
