import serial
import matplotlib.pyplot as plt
import time
from scipy.optimize import curve_fit
import numpy as np

# Daten einlesen
ser = serial.Serial('/dev/ttyACM4', 250000)
time.sleep(1)  # 1 Sekunden warten, damit die Verbindung stabil ist
ser.reset_input_buffer()  # Puffer leeren

times = []
values = []
print("Warte auf Daten...")

while len(values) < 2000:
    line = ser.readline().decode(errors='ignore').strip()
    if ',' in line:
        try:
            t_str, v_str = line.split(",")
            times.append(int(t_str))
            values.append(int(v_str))
        except Exception as e:
            print(f"Fehler beim Verarbeiten der Zeile: {e}")
            pass
t = (np.array(times) - times[0]) / 1000  # us → ms
V = np.array(values)

ser.close()


#dt = .3 # 1ms pro Messpunkt
#V = np.array(data) 
#t = np.arange(len(V)) * dt  # Zeitachse

def plot_data(t, V):
    plt.plot(t, V)
    plt.xlabel('Zeit (ms)')
    plt.ylabel('ADC-Wert')
    plt.ylim(0, 1023)
    plt.grid()
    plt.show()

plot_data(t, V)

# === Parameter zur Flankenerkennung ===
MIN_DROP = 50  # Mindestabfall, um eine Flanke zu erkennen
MIN_LEN = 5  # Mindestlänge einer Flanke

# === Funktion für RC-Entladungskurve ===
def rc_discharge(t, V0, tau):
    return V0 * np.exp(-t / tau)

# === Flanken extrahieren ===

falling_flanks = []
current_flank_idx = []

for i in range(1, len(V)):
    if V[i] < V[i-1]:
        current_flank_idx.append(i-1)
    else:
        if current_flank_idx:
            current_flank_idx.append(i-1)
            start_idx = current_flank_idx[0]
            end_idx = current_flank_idx[-1]
            #current_flank = V[start_idx:end_idx+1]
            if (V[start_idx] - V[end_idx] >= MIN_DROP) and (len(current_flank_idx) >= MIN_LEN):
                falling_flanks.append((start_idx, end_idx))
            current_flank_idx = []

# letzte Flanke prüfen
if current_flank_idx:
    current_flank_idx.append(len(V)-1)
    start_idx = current_flank_idx[0]
    end_idx = current_flank_idx[-1]

    if (V[start_idx] - V[end_idx] >= MIN_DROP) and (len(current_flank_idx) >= MIN_LEN):
        falling_flanks.append((start_idx, end_idx))

print(f"Gefundene Flanken: {len(falling_flanks)}")
for idx, (start_idx, end_idx) in enumerate(falling_flanks):
    V_flank = V[start_idx:end_idx]
    t_flank = t[start_idx:end_idx]
    t_flank = t_flank - t_flank[0]  # Zeit auf 0 setzen
    tau = t_flank[-1]/np.log(V_flank[0]/V_flank[-1])  # Tau berechnen
    print(tau)

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


