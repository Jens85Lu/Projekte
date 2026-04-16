import serial
import matplotlib.pyplot as plt

ser = serial.Serial('/dev/ttyACM3', 115200)  # ggf. anpassen

times = []
values = []
print("Warte auf Daten...")
while True:
    line = ser.readline().decode().strip()
    print(line)
    if line == "END" and not values == []: 
        break

    try:
        t, v = line.split(",")
        if int(v) == 0: continue
        times.append(float(t) / 1e6)  # µs → s
        values.append(int(v))
    except:
        pass

# Berechene tau nach der der Maximalwert values[0] auf 1/e abfällt aus t und values
max_value = values[0]
tau = None
for t, v in zip(times, values):
    if v <= max_value / 2.71828:  # 1/e ≈ 0.3679
        tau = t
        break
print(f"Abklingzeit τ: {tau:.6f} s")



plt.plot(times, values)
plt.xlabel("Zeit (s)")
plt.ylabel("ADC Wert")
plt.title("Abklingkurve")
plt.grid()
plt.show()