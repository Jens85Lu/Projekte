import serial
import matplotlib.pyplot as plt
import time
from scipy.optimize import curve_fit
import numpy as np

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


dt = 0.1 # 0.1ms pro Messpunkt
V = np.array(data) 
t = np.arange(len(V)) * dt  # Zeitachse, 0.01 Sekunden pro Messpunkt

def plot_data(data):
    plt.plot(t, V)
    plt.xlabel('Zeit (ms)')
    plt.ylabel('ADC-Wert')
    plt.ylim(0, 1023)
    plt.grid()
    plt.show()

plot_data(data)

# === Parameter zur Flankenerkennung ===
MIN_DROP = 50  # Mindestabfall, um eine Flanke zu erkennen
MIN_LEN = 5  # Mindestlänge einer Flanke

# === Funktion für RC-Entladungskurve ===
def rc_discharge(t, V0, tau):
    return V0 * np.exp(-t / tau)

# === Flanken extrahieren ===

falling_flanks = []
current_flank = []

for i in range(1, len(V)):
    if V[i] < V[i-1]:
        current_flank.append(V[i-1])
    else:
        if current_flank:
            current_flank.append(V[i-1])  # Letzten Wert der Flanke hinzufügen
            if (current_flank[0] - current_flank[-1] >= MIN_DROP) and (len(current_flank) >= MIN_LEN):
                falling_flanks.append(np.array(current_flank))
            current_flank = []

# letzte Flanke prüfen
if current_flank:
    current_flank.append(V[-1])
    if (current_flank[0] - current_flank[-1] >= MIN_DROP) and (len(current_flank) >= MIN_LEN):
        falling_flanks.append(np.array(current_flank))

print(f"Gefundene Flanken: {len(falling_flanks)}")

# === Fit jeder Flanke mit curve_fit===
def nonlinear_fit(falling_flanks, dt):
    taus = []
    plt.figure(figsize=(10, 6))
    for idx, flank in enumerate(falling_flanks):
        flank = flank[2:]  # Ersten Wert entfernen, da er nicht zur Flanke gehört
        t_flank = np.arange(len(flank)) * dt
        try:
            popt, _ = curve_fit(rc_discharge, t_flank, flank, p0=(flank[0], 1))
            taus.append(popt[1])
            print(f"Flanke {idx}: Tau = {popt[1]:.4f} Millisekunden")
            plt.plot(t_flank, flank, color='blue', alpha=0.5)
            plt.plot(t_flank, rc_discharge(t_flank, *popt), color='red', linestyle='--' )
        except RuntimeError:
            print(f"Fit für Flanke {idx} fehlgeschlagen.")

    plt.xlabel('Zeit (ms)')
    plt.ylabel('Spannung (ADC-Wert)')
    plt.title('Gefundene fallende Flanken und ihre Fits')
    plt.grid()
    plt.show()
    print("Durchschnittliche Zeitkonstante (nonlinear fit) tau:", np.mean(taus))


#nonlinear_fit(falling_flanks, dt)   

def histogram_taus(taus):
    plt.figure(figsize=(6,4))
    plt.hist(taus, bins=10, color='green', alpha=0.7)
    plt.xlabel("Tau [ms]")
    plt.ylabel("Anzahl der Flanken")
    plt.title("Verteilung der Zeitkonstanten")
    plt.show()
#histogram_taus(taus)

### Flanken mit linearisierter Funktion fitten
def linearized_fit(falling_flanks, dt):
    taus = []
    intercepts = []
    plt.figure(figsize=(10, 6))
    for idx, flank in enumerate(falling_flanks):
        flank = flank[4:-4]  # Ersten Wert entfernen, da er nicht zur Flanke gehört
        t_flank = np.arange(len(flank)) * dt
        V_flank = flank
        y = np.log(V_flank)  # Normalisieren und logarithmieren
        x = t_flank
        coeff  = np.polyfit(x, y, 1)
        slope = coeff[0]
        intercept = coeff[1]
        tau = -1/slope
        ### Hier werden später noch die Residuen berechnet, um die Qualität des Fits zu bewerten
        plt.plot(x, y, '+', color='blue', alpha=0.5)
        plt.plot(x, intercept + slope * x, color='red', linestyle='--' )
        print(f"Flanke {idx}: Tau (linearisiert) = {tau:.4f} Millisekunden")
        taus.append(tau)
        intercepts.append(intercept)
        residuals = y - (intercept + slope * x)
        SSR = np.sum(residuals**2) # Summe der quadrierten Residuen
        sigma = np.sqrt(SSR / (len(x) - 2))
        SST = np.sum((y - np.mean(y))**2) # Totale Summe der Quadrate
        R_squared = 1 - (SSR / SST) # Bestimmtheitsmaß R², je näher bei 1, desto besser der Fit
        print(f"Flanke {idx}: R² = {R_squared:.4f}")
    
    plt.xlabel('Zeit (ms)')
    plt.ylabel('Spannung (ADC-Wert)')
    plt.title('Gefundene fallende Flanken und ihre linearen Fits')
    plt.grid()
    plt.show()
    print(f"Durchschnittliche Zeitkonstante (linearisiert) tau:", np.mean(tau))
    return taus, intercepts

#taus, intercepts = linearized_fit(falling_flanks, dt)


