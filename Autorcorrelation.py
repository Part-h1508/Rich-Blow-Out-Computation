"""
this file is to simulate autocorrelation for RBO (final corrected)
the graph describes temporal behaviour of the signal

updated based on prof feedback:
--> using short segment (2 sec)
--> correct normalization (r(0) = 1)
--> smoothing without affecting first point
--> reduced lag window for better visualization
"""

# imports
import numpy as np
import matplotlib.pyplot as plt
import os

# variables
folder_path = "."
phi_rbo = 6.3

# files to compare
plot_files = ["5.0.txt", "5.8.txt", "6.3.txt"]

plt.figure(figsize=(10, 6))

for file in plot_files:
    
    file_path = os.path.join(folder_path, file)
    
    # load data
    data = np.loadtxt(file_path)
    time = data[:, 0]
    signal = data[:, 1]

    # remove mean
    signal = signal - np.mean(signal)

    # sampling frequency
    dt = time[1] - time[0]
    fs = 1 / dt

    # use only first 2 seconds
    signal = signal[:int(2 * fs)]

    # autocorrelation
    corr = np.correlate(signal, signal, mode='full')
    center = corr.size // 2

    # shorter lag window (20 ms)
    max_lag = int(0.02 * fs)

    rxx = corr[center:center + max_lag] / corr[center]

    # smooth ONLY after first few points
    smooth = np.copy(rxx)

    # apply smoothing starting from index 2
    smooth[2:] = np.convolve(rxx[2:], np.ones(5)/5, mode='same')

    # enforce correct normalization
    smooth[0] = 1
    smooth[1] = rxx[1]

    rxx = smooth

    # lag axis
    lag = (np.arange(max_lag) / fs) * 1000

    # normalized ratio
    fuel_val = float(file.replace(".txt", ""))
    phi_norm = fuel_val / phi_rbo

    # plot
    plt.plot(lag, rxx, label=f"Φ/Φ_RBO = {phi_norm:.3f}")

# formatting
plt.xlabel("Lag Time (ms)")
plt.ylabel("Autocorrelation Coefficient")

plt.axhline(0, color='black', linewidth=1, alpha=0.5)
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig("Figure_RBO_Autocorr_FINAL.png", dpi=300)
plt.show()