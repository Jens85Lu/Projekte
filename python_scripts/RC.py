import numpy as np 
import matplotlib.pyplot as plt
import serial
import time

# Daten einlesen
ser = serial.Serial('/dev/ttyACM3', 115200)
time.sleep(1)  # 1 Sekunden warten, damit die Verbindung stabil ist
ser.reset_input_buffer()  # Puffer leeren

data = []

plt.ion()

fig, ax1  = plt.subplots(figsize=(5, 3))

while True:
    line = ser.readline().decode().strip()
    print(f"Gelesene Zeile: '{line}'")  # Debug-Ausgabe der gelesenen Zeile
    try:
        data.append(float(line))
    except Exception as e:
        print(f"Fehler beim Konvertieren der Zeile: {e}")
        pass

    if len(data) > 100:
        data = data[-100:]  # Nur die letzten 100 Werte behalten
    ax1.clear()
    ax1.plot(data)
    ax1.set_xlim(0, 100)
    ax1.set_ylim(0.95, 1.05)
    ax1.set_title('Echtzeitdaten')
    ax1.set_xlabel('Messpunkt')
    ax1.set_ylabel('Signal')
    plt.pause(0.01)

