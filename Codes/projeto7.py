import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz, lfilter
import librosa
import sounddevice as sd
import time
import os

def peaking_eq(f0, gain_db, Q, fs):

    A = 10**(gain_db / 40)  #amplitude
    omega = 2 * np.pi * f0 / fs
    alpha = np.sin(omega) / (2 * Q)

    b0 = 1 + alpha * A
    b1 = -2 * np.cos(omega)
    b2 = 1 - alpha * A
    a0 = 1 + alpha / A
    a1 = -2 * np.cos(omega)
    a2 = 1 - alpha / A

    b = np.array([b0, b1, b2]) / a0
    a = np.array([1.0, a1/a0, a2/a0])
    return b, a

def load_audio(file_path):
    try:
        audio, sr = librosa.load(file_path, sr=None)
        return audio, sr
    except Exception as e:
        print(f"Erro carregando o arquivo: {e}")
        return None, None

def apply_filters(audio, filters):
    filtered_audio = audio.copy()
    for b, a in filters:
        filtered_audio = lfilter(b, a, filtered_audio)
    
    #evita clipping aq
    max_val = np.max(np.abs(filtered_audio))
    if max_val > 1.0:
        filtered_audio = filtered_audio / max_val
    
    return filtered_audio

def get_overall_response(filters, fs, n_points=8192):
    freqs = np.linspace(0, fs/2, n_points)
    overall_response = np.ones(n_points, dtype=complex)
    
    for b, a in filters:
        _, h = freqz(b, a, worN=n_points, fs=fs)
        overall_response *= h
    
    return freqs, overall_response

def plot_bode_diagram(filters, fs):
    freqs, overall_response = get_overall_response(filters, fs)
    
    plt.figure(figsize=(10, 6))
    plt.semilogx(freqs, 20 * np.log10(np.abs(overall_response)))
    plt.title('Overall Equalizer Response (Bode Diagram)')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Gain [dB]')
    plt.grid(True, which="both", ls="-")
    plt.axhline(y=0, color='k', linestyle='-')
    plt.xlim(20, fs/2)
    plt.yticks(np.arange(-12, 13, 2))
    plt.show()

def main():
    #12 bandas (freqs)
    bands = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 10000, 16000, 20000]
    
    file_path = "Codes/direstraits.mp3"
    
    if not os.path.exists(file_path):
        print(f"Erro: File {file_path} não encontrada!")
        return
    
    print(f"Audio file: {file_path}")
    audio, sr = load_audio(file_path)
    if audio is None:
        return
    
    print(f"Sample rate: {sr} Hz, Duração: {len(audio)/sr:.2f} segundos")
    
    #inputs pras bandas
    gains = []
    print("\nGanhos do equalizador (-10dB to +10dB):\n")
    for band in bands:
        while True:
            try:
                gain = float(input(f"Ganho de {band} Hz (-10 até +10 dB): "))
                if -10 <= gain <= 10:
                    gains.append(gain)
                    break
                else:
                    print("Tem que ser entre -10 e +10 dB.")
            except ValueError:
                print("Inválido.")
    
    #Cria filtros pras bandas
    filters = []
    Q = 1.0  #QF
    for band, gain in zip(bands, gains):
        if abs(gain) > 0.01:  #Só cria filtro se o ganho for significativo
            b, a = peaking_eq(band, gain, Q, sr)
            filters.append((b, a))
    
    if not filters:
        print("No filters applied (all gains set to 0).")
        return
    
    #aplica o filtro
    print("\nApplying filters...")
    filtered_audio = apply_filters(audio, filters)
    
    #Plota o Bode
    print("\nGenerating Bode diagram...")
    plot_bode_diagram(filters, sr)
    
    #Toca o audio original
    print("\nPlaying original audio...")
    sd.play(audio, sr)
    sd.wait()
    
    #1 sec
    print("\nWaiting 1 second...")
    time.sleep(1)
    
    #Toca o audio filtrado
    print("\nPlaying filtered audio...")
    sd.play(filtered_audio, sr)
    sd.wait()

#main
if __name__ == "__main__":
    main()
