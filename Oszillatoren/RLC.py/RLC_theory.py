import numpy as np
import matplotlib.pyplot as plt




R = 1.7 # Widerstand in Ohm
L = 0.00051 # Induktivität in Henry 1mH
C = 0.000047 # Kapazität in Farad 22µF

# Zeitliche Entwicklung der Kondensatorspannung bei V(0) = 5V und I(0) = 0A numerisch berechnen als Lösung der DGL: L*d²V/dt² + R*dV/dt + V/C = 0
def V(t, R=R, L=L, C=C):
    alpha = R/(2*L)
    omega_0 = 1/np.sqrt(L*C)
    if alpha < omega_0: # Unterkritisch
        omega_d = np.sqrt(omega_0**2 - alpha**2)
        return 5 * np.exp(-alpha*t) * (np.cos(omega_d*t) + (alpha/omega_d)*np.sin(omega_d*t))
    elif alpha == omega_0: # Kritisch
        return 5 * np.exp(-alpha*t) * (1 + alpha*t)
    else: # Überkritisch
        s1 = -alpha + np.sqrt(alpha**2 - omega_0**2)
        s2 = -alpha - np.sqrt(alpha**2 - omega_0**2)
        A = 5*(s2 + alpha) / (s2 - s1)
        B = 5*(s1 + alpha) / (s1 - s2)
        return A * np.exp(s1*t) + B * np.exp(s2*t)

#ω = np.linspace(0, 10000, 1000) # Frequenzbereich von 0 bis 10 kHz


# Zeitliche Entwicklung der Spannung plotten für 
plt.subplot(2, 1, 1)
t = np.linspace(0, 0.05, 500) # Zeit von 0 bis 100 ms
#plt.plot(t, V(t, R=1, L=L, C=C))
plt.plot(t, V(t, R=R, L=L, C=C), 'o') # blaue Farbe mit roten Punkten
#plt.plot(t, V(t, R=4, L=L, C=C))
#plt.plot(t, V(t, R=6, L=L, C=C))
#plt.plot(t, V(t, R=8, L=L, C=C))
plt.legend(['R={}'.format(R)])
plt.title('Spannung eines RLC-Kreises')
plt.xlim(0, 0.10/5)
plt.xlabel('Zeit (s)')
plt.ylabel('Spannung (V)')
plt.grid()


# FFT der Spannung plotten für R=1.5Ω
fft = np.fft.fft(V(t, R=R, L=L, C=C))
freqs = np.fft.fftfreq(len(t), t[1]-t[0])
print(np.diff(freqs)) # Frequenzauflösung der FFT

plt.subplot(2, 1, 2)
plt.plot(freqs[:len(freqs)//2], np.abs(fft[:len(fft)//2]))
# doppellogarithmische Darstellung
#plt.xscale('log')
#plt.yscale('log')
plt.xlabel('Frequenz (Hz)')
plt.ylabel('Magnitude')
plt.title('FFT der Spannung für R={}Ω'.format(R))
plt.grid()

plt.show()