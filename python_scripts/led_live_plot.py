import serial
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time

# ---- Einstellungen ----
PORT = "/dev/ttyACM3"
BAUD = 115200

ser = serial.Serial(PORT, BAUD)
#time.sleep(2)
#ser.reset_input_buffer()

U_vals = []
I_vals = []

plt.ion()
fig, ax = plt.subplots()
plt.show(block=False)
plt.pause(0.1)

def shockley(U, Is, n):
    Ut = 0.02585  # thermische Spannung
    return Is * np.exp((U/(n*Ut)) - 1)

def diode_model(I, Is, n, Rs):
    Ut = 0.02585  # thermische Spannung
    return np.log(1 + I/Is) * n * Ut + I * Rs

while True:
    line = ser.readline().decode().strip()
    
    try:
        U, I = map(float, line.split(","))
        #U, I = map(float, map(str.strip, line.split(",")))
    except:
        continue

    if I <= -1 or U > 5:
        continue

    U_vals.append(U)
    I_vals.append(I)
    print(f"U: {U:.3f} V, I: {I:.6f} A")

    ax.clear()
    ax.plot(U_vals, I_vals, 'o', label="Messung")

    # Fit nur innerhalb eines sinnvollen Bereichs durchführen
    U_fit = np.array(U_vals)
    I_fit = np.array(I_vals)

    mask = (0.00001 < I_fit) & (I_fit < 0.008)  # Bereich für den Fit
    if np.sum(mask) > 5:
        try:
            popt, _ = curve_fit(shockley, U_fit[mask], I_fit[mask],
                                p0=[1e-9, 2])

            Is, n = popt
            Rs = 0  # Rs ist nicht im Shockley-Modell enthalten
            #print(f"Fit-Parameter: Is={Is:.2e}, n={n:.2f}, Rs={Rs:.2f}")

            U_fit = np.linspace(min(U_fit[mask]), max(U_fit[mask]), 200)
            I_fit = shockley(U_fit, Is, n)

            #ax.plot(U_fit, I_fit, label=f"Shokley Fit\nIs={Is:.2e}, n={n:.2f}")

        except:
            pass

    ax.set_xlabel("U_LED (V)")
    ax.set_ylabel("I (A)")
    ax.set_title("LED Kennlinie")
    ax.legend()
    plt.pause(0.01)
