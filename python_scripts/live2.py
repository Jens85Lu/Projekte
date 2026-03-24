import serial
import numpy as np
import matplotlib.pyplot as plt
import time

port = "/dev/ttyACM3"
baud = 115200

samples = 512
fs = 1000

ser = serial.Serial(port, baud)
time.sleep(2)
ser.reset_input_buffer()

buffer = []

plt.ion()
fig, (ax1, ax2) = plt.subplots(1,2)

while True:

    line = ser.readline().decode(errors="ignore").strip()

    try:
        value = int(line)
        buffer.append(value)

    except:
        continue

    if len(buffer) >= samples:

        data = np.array(buffer[:samples])
        buffer = buffer[samples:]   # alte Daten entfernen

        # FFT
        data = data - np.mean(data)
        fft = np.fft.fft(data)
        freqs = np.fft.fftfreq(samples, 1/fs)

        magnitude = np.abs(fft)

        ax1.clear()
        ax2.clear()

        ax1.plot(data)
        ax1.set_title("Signal")

        ax2.plot(freqs[:samples//2], magnitude[:samples//2])
        ax2.set_title("FFT")

        plt.pause(0.001)