import numpy as np 
import matplotlib.pyplot as plt
import serial
import time

# Rechtecksignal mit 5 Hz und 50% Duty Cycle erzeugen
fs = 10000 # Abtastfrequenz
f = 5 # Frequenz des Rechtecksignals
t = np.arange(0, 1, 1/fs) # Zeitachse von 0 bis 1 Sekunde
signal = 0.5 * (1 + np.sign(np.sin(2 * np.pi * f * t))) # Rechtecksignal mit Amplitude von 1 und 0
V = signal * 1023 # Skalieren auf ADC-Werte (0-1023)


# Daten einlesen
ser = serial.Serial('/dev/ttyACM3', 250000)
time.sleep(1)  # 1 Sekunden warten, damit die Verbindung stabil ist
ser.reset_input_buffer()  # Puffer leeren

data = []

while len(data) < 10000:
    line = ser.readline().decode(errors='ignore').strip()
    if line.isdigit():  # Überprüfen, ob die Zeile eine Zahl ist
        data.append(int(line))

ser.close()
W = np.array(data)
#W = V

dt = 0.0001 # 0.1ms pro Messpunkt
fs = 1/dt # Abtastfrequenz
N = len(V) # Anzahl der Messpunkte
M = len(W) # Anzahl der Messpunkte
print(M-N)  # Überprüfen, ob die Anzahl der Messpunkte übereinstimmt

tau = 0.001 # Zeitkonstante des RC-Filters
alpha = dt/tau

# RC-Filter anwenden
y = np.zeros_like(W)
y[0] = W[0] # Startwert
for i in range(1, M):
    y[i] = y[i-1] + alpha * (W[i] - y[i-1]) # RC-Filter anwenden

V = W # Originalsignal
W = y # Gefiltertes Signal


# FFT berechnen
V = V - np.mean(V) # Mittelwert entfernen
W = W - np.mean(W) # Mittelwert entfernen
X = np.fft.fft(V)
Y = np.fft.fft(W)

# Frequenzachse erstellen
freq = np.fft.fftfreq(N, d=dt)


# Nur positive Frequenzen betrachten
mask = freq > 0
freq = freq[mask]
X = X[mask]
Y = Y[mask]
# Amplitudenspektrum berechnen
amplitude = np.abs(X) / N
amplitude_W = np.abs(Y) / M

H = amplitude_W / amplitude
plt.plot(freq, H)
plt.xlabel('Frequenz (Hz)')
plt.ylabel('Frequenzgang')
plt.xlim(0, 1000) # Frequenzbereich begrenzen
plt.grid()
plt.show()

plt.plot(freq,amplitude, label='Originalsignal')
plt.plot(freq, amplitude_W, label='Gefiltertes Signal')
plt.xlabel('Frequenz (Hz)')
plt.ylabel('Amplitude')
plt.xlim(0, 1000) # Frequenzbereich begrenzen
plt.grid()
plt.legend()
plt.show()

