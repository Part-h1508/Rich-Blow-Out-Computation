"""
this file is to simulate the 2nd figure (RBO)
the graph describes physical behaviour of the frequencies

The fig includes:

Frequency spectrum (PSD) for RBO precursors.
The legend shows normalized fuel ratio (Φ/Φ_RBO).

We find:
--> dominant energy lies in low frequency region (< 50 Hz)
--> as we approach RBO, energy becomes more concentrated
--> a clear peak appears indicating slow oscillatory behaviour
"""

"""
similar to LBO, prof wants us to focus on low frequency region.
so we zoom till 100 Hz and smoothen the PSD a bit
to remove unnecessary noise from high resolution.
"""

# imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
import os

# plot settings (same style as before)
plt.rcParams.update({
    "font.size": 16,
    "axes.labelsize": 18,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 14
})

# variables
phi_rbo = 6.3

# choose 3 cases: low, mid, near RBO
plot_files = ["5.0.txt", "5.8.txt", "6.3.txt"]

plt.figure(figsize=(10, 6))

for file in plot_files:
    
    file_path = file
    
    # load data
    data = np.loadtxt(file_path)
    time = data[:, 0]
    signal = data[:, 1]
    
    # remove DC offset (important)
    signal = signal - np.mean(signal)
    
    # sampling frequency
    delta_t = time[1] - time[0]
    fs = 1 / delta_t

    # compute PSD (keep nperseg same as LBO for smoothness)
    frequencies, psd = welch(signal, fs=fs, nperseg=4096)

    # small smoothing to reduce noise
    psd = np.convolve(psd, np.ones(5)/5, mode='same')

    # normalized fuel ratio
    fuel_val = float(file.replace(".txt", ""))
    phi_norm = fuel_val / phi_rbo

    # plot
    plt.semilogy(frequencies, psd, label=f"Φ/Φ_RBO = {phi_norm:.3f}")

    # find peak (ignore DC)
    peak_index = np.argmax(psd[1:]) + 1
    peak_freq = frequencies[peak_index]
    peak_power = psd[peak_index]

    # mark peak
    plt.plot(peak_freq, peak_power, 'ro')

    plt.annotate(
        f"{peak_freq:.1f} Hz",
        xy=(peak_freq, peak_power),
        xytext=(peak_freq + 10, peak_power * 2),
        fontsize=12,
        arrowprops=dict(arrowstyle="->")
    )

# formatting
plt.xlabel("Frequency (Hz)")
plt.ylabel("PSD")
plt.xlim(0, 100)   # same zoom as LBO
plt.grid(True, alpha=0.3)
plt.legend(title="Φ/Φ_RBO")

plt.tight_layout()
plt.savefig("Figure_2_RBO_FrequencySpectrum.png", dpi=300)
plt.show()