import numpy as np
import matplotlib.pyplot as plt

# ----- Parameter -----
T0 = 1.0  # Abtastzeit
k = np.arange(0, 20)  # 20 Abtastpunkte

# ----- Exakte Sprunginvarianz -----
# G(z) = 0.9 z^-1 / (1 - 0.82 z^-1)
y_exact = 0.9 * (1 - 0.82**k) / (1 - 0.82)

# ----- Bilineare Transformation (Tustin) -----
# G(z) = 0.4545 * (1 + z^-1) / (1 - 0.8182 z^-1)
b0 = 0.4545
b1 = 0.4545
a1 = 0.8182

y_bilinear = np.zeros_like(k, dtype=float)
for i in range(len(k)):
    if i == 0:
        y_bilinear[i] = b0  # Initialwert
    else:
        y_bilinear[i] = b0 + b1 + a1 * y_bilinear[i-1]

# ----- Plot -----
plt.figure(figsize=(10,5))
plt.stem(k, y_exact, linefmt='b-', markerfmt='bo', basefmt=" ", label='Exakte Sprunginvarianz')
plt.stem(k, y_bilinear, linefmt='r--', markerfmt='rx', basefmt=" ", label='Bilineare Transformation')
plt.xlabel('k (Abtastpunkte)')
plt.ylabel('Sprungantwort y(k)')
plt.title('Vergleich Sprungantwort: Exakt vs. Bilinear')
plt.legend()
plt.grid(True)
plt.show()