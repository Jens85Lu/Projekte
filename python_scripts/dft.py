# Matplotlib und Numpy importieren
import numpy as np
import matplotlib.pyplot as plt


# Diskrete Zeitachse mit 8 Punkten
N = 8
n = np.arange(N)
# Sinussignal mit mit Frequenz 2 mal die Abtastfrequenz
f = 2
x = np.sin(2 * np.pi * f * n / N)

M = N-1
m = np.arange(M)
y = np.sin(2 * np.pi * f * m / M)
W = np.exp(-2j * np.pi * np.outer(m, m) / M)
Y = W @ y
plt.stem(m, np.abs(Y))
plt.xlabel('k')
plt.ylabel('|Y[k]|')
plt.title('DFT des Sinussignals mit Länge M=N-1')
plt.grid()

# Fourier Matrix erstellen
W = np.exp(-2j * np.pi * np.outer(n, n) / N)


# DFT berechnen
X = W @ x
# Plotten der DFT symmetisch um Null auf der Frequenzachse

plt.stem(n, np.abs(X))
plt.xlabel('k')
plt.ylabel('|X[k]|')
plt.title('DFT des Sinussignals')
plt.xlim(0, 8)
plt.grid()
plt.show()



# # Plotten des Sinussignals
# plt.stem(n, x)
# plt.xlabel('n')
# plt.ylabel('x[n]')
# plt.title('Diskretes Sinussignal')
# plt.grid()
# plt.show()