import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment
import os

# Configurações
duracao = 10  # segundos
frequencia_amostragem = 44100  # Hz
arquivo_wav = "gravacao_temp.wav"
arquivo_mp3 = "gravacao_final.mp3"

print("Gravando...")
audio = sd.rec(int(duracao * frequencia_amostragem), samplerate=frequencia_amostragem, channels=1, dtype='int16')
sd.wait()
print("Gravação concluída!")

# Salva WAV temporário
write(arquivo_wav, frequencia_amostragem, audio)

# Converte para MP3
som = AudioSegment.from_wav(arquivo_wav)
som.export(arquivo_mp3, format="mp3")
print(f"Arquivo salvo como: {arquivo_mp3}")

# Remove o WAV temporário
os.remove(arquivo_wav)
