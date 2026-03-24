import serial
import numpy as np
import matplotlib.pyplot as plt
import time

port = '/dev/ttyACM3'
baud = 460800
samples = 512
fs = 2000

ser = serial.Serial(port, baud)
time.sleep(2)
ser.reset_input_buffer()

plt.ion()
fig, (ax1, ax2) = plt.subplots(1,2,figsize=(8,4))

while True:

    # exakt samples*2 Bytes einlesen
    data_bytes = bytearray()
    while len(data_bytes) < samples*2:
        data_bytes += ser.read(samples*2 - len(data_bytes))

    data = np.frombuffer(data_bytes, dtype=np.uint16)

    # in Volt umrechnen
    data = data * (5.0 / 1023.0)

    t = np.arange(samples) / fs * 1000

    # FFT
    fft_vals = np.fft.fft(data - np.mean(data))
    fft_vals = fft_vals / samples
    freqs = np.fft.fftfreq(samples, 1/fs)
    magnitude = np.abs(fft_vals)

    ax1.clear()
    ax1.plot(t, data)
    ax1.set_xlabel("Zeit (ms)")
    ax1.set_ylabel("Spannung (V)")
    ax1.set_title("Zeitbereich")

    ax2.clear()
    ax2.plot(freqs[:samples//2], magnitude[:samples//2])
    ax2.set_xlim(0, fs/2)
    ax2.set_xlabel("Frequenz (Hz)")
    ax2.set_title("FFT")

    plt.pause(0.01)