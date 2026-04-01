"""
Autocorrelation plot for RBO (corrected & defensible)

Fixes applied:
- Proper normalization so r(0) = 1
- Removed smoothing (avoids distortion of ACF)
- Uses short segment (2 sec) for local behaviour
- Clean and physically correct implementation
"""

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

    # sampling frequency
    dt = time[1] - time[0]
    fs = 1 / dt

    # remove mean
    signal = signal - np.mean(signal)

    # use only first 2 seconds
    N = int(2 * fs)
    signal = signal[:N]

    # autocorrelation
    corr = np.correlate(signal, signal, mode='full')
    center = len(corr) // 2

    # normalize → ensures r(0) = 1
    corr = corr / corr[center]

    # shorter lag window (20 ms)
    max_lag = int(0.02 * fs)
    rxx = corr[center:center + max_lag]

    # lag axis
    lag = (np.arange(max_lag) / fs) * 1000

    # normalized equivalence ratio
    fuel_val = float(file.replace(".txt", ""))
    phi_norm = fuel_val / phi_rbo

    # plot
    plt.plot(lag, rxx, label=f"$\\Phi/\\Phi_{{RBO}}$ = {phi_norm:.3f}")

# formatting
plt.xlabel("Lag Time (ms)")
plt.ylabel("Autocorrelation Coefficient")

plt.axhline(0, color='black', linewidth=1, alpha=0.5)
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig("Figure_RBO_Autocorr_FINA1L.png", dpi=300)
plt.show()