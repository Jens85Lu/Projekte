import serial
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ---- Einstellungen ----
PORT = "/dev/ttyACM3"
BAUD = 115200

ser = serial.Serial(PORT, BAUD)

U_vals = []
I_vals = []

plt.ion()
fig, ax = plt.subplots()


while True:
    line = ser.readline().decode().strip()
    
    try:
        U, I = map(float, line.split(","))
        I = I*1000 # Umrechnung von A in mA
        #U, I = map(float, map(str.strip, line.split(",")))
    except:
        continue

    if I <= 0:
        continue

    U_vals.append(U)
    I_vals.append(I)
    print(f"U: {U:.3f} V, I: {I:.6f} A")

    ax.clear()
    ax.plot(U_vals, I_vals, 'o', label="Messung")

  
    ax.set_xlabel("U_LED (V)")
    ax.set_ylabel("I (mA)")
    ax.set_title("Solarzellen Kennlinie")
    ax.legend()
    ax.grid()
    plt.pause(0.01)
