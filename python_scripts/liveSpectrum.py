# Pin 9 wird an A0 angeschlossen, um das Signal zu messen.
# Das Signal wird über die serielle Schnittstelle an den
# Computer gesendet und in Echtzeit geplottet.
# Die linke Grafik zeigt das Signal im Zeitbereich,
# während die rechte Grafik die Magnitude der FFT im Frequenzbereich
# darstellt

# Importieren der benötigten Bibliotheken
import serial
import numpy as np
import matplotlib.pyplot as plt

port = '/dev/ttyACM3'
baud = 115200
samples = 512
fs = 1200  # Abtastfrequenz in Hz

ser = serial.Serial(port, baud)
import time
time.sleep(2)  # Warte auf die Verbindung

plt.ion()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5, 3))

while True:
    data = []

    while len(data) < samples:
        line = ser.readline().decode().strip()
        try:
            data.append(int(line))
        except:
            pass

    data = np.array(data)
    data = data * (5.0 / 1023.0)  # Umrechnung in Volt (10-bit ADC, 5V Referenz)
    #data = data - np.mean(data)  # DC-Offset entfernen
    t = np.arange(samples) / fs * 1000  # Zeit in ms

    # FFT
    fft = np.fft.fft(data-np.mean(data))
    fft = fft / samples  # Normalisieren
    freqs = np.fft.fftfreq(samples, 1/fs)
    magnitude = np.abs(fft)

    ax1.clear()
    ax2.clear()
    ax1.plot(t[:samples//10], data[:samples//10])
    ax1.set_title('Signal (Zeitbereich)')
    ax1.set_xlabel('Zeit (ms)')
    
    ax2.plot(freqs[:samples//2], magnitude[:samples//2])
    ax2.set_title('Magnitude (Frequenzbereich)')
    ax2.set_xlabel('Frequenz (Hz)')
    ax2.set_xlim(0, fs/2)

    plt.pause(0.01)
