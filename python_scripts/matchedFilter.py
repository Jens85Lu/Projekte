import numpy as np
import matplotlib.pyplot as plt

# Zeitachse
fs = 1000  # Abtastfrequenz
t = np.linspace(0, 1, fs, endpoint=False)  # 1 Sekunde

# Pulsform (exponentieller Anstieg und Abfall)
def pulse(t, tau_r=0.01, tau_f=0.05):
    return (1-np.exp(-t/tau_r)) * np.exp(-t/tau_f)

# Signal erzeugen, periodischer Puls alle 0.2 Sekunden
s = np.zeros_like(t)
for i in range(0, len(t), int(0.2*fs)):
    s[i:i+int(0.1*fs)] += pulse(t[:int(0.1*fs)])
#s = pulse(t)
# Weißes Rauschen
noise = 1.05*np.random.randn(len(t))
# Gesamtsignal
x = s + noise

# Zeitgespiegelte Pulsform
s_mf = s[::-1]  # Zeitgespiegelt
# Faltung des Eingangssignals mit der zeitgespiegelten Pulsform
y = np.convolve(x, s_mf, mode='same')

# Erstellen der Subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 8))

# Erster Plot: Signal mit Rauschen und Originalsignal
axs[0].plot(t, x, label='Signal mit Rauschen')
axs[0].plot(t, s, label='Originalsignal', linewidth=2)
axs[0].set_xlabel('Zeit (s)')
axs[0].set_ylabel('Amplitude')
axs[0].set_title('Signal mit Rauschen')
axs[0].legend()
axs[0].grid()

# Zweiter Plot: Matched Filter Output
axs[1].plot(y, label='Matched Filter Output')
axs[1].set_xlabel('Zeit (s)')
axs[1].set_ylabel('Amplitude')
axs[1].set_title('Matched Filter Output')
axs[1].legend()
axs[1].grid()

# Layout anpassen und anzeigen
plt.tight_layout()
plt.show()

peak_index = np.argmax(y)
peak_value = y[peak_index]
print(f'Peak bei Index {peak_index}, Wert {peak_value}')