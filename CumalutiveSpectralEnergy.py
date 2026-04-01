"""
this file is to simulate the cumulative spectral energy for RBO
the graph describes how energy is distributed across frequencies

The fig includes:

Cumulative spectral energy plots for three fuel conditions

We find:
--> energy accumulates faster in low frequency region
--> behaviour changes as we approach RBO
"""

"""
same method as before.
we take FFT, compute amplitude squared and then cumulative sum.
finally normalize it so it goes from 0 to 1.
"""

# imports
import numpy as np
import matplotlib.pyplot as plt
import os

# plot settings for larger fonts
plt.rcParams.update({
    "font.size": 20,
    "axes.labelsize": 20,
    "xtick.labelsize": 20,
    "ytick.labelsize": 20,
    "axes.titlesize": 20
})

# variables
phi_rbo = 6.3

# choose same 3 cases
plot_files = ["5.0.txt", "5.8.txt", "6.3.txt"]

plt.figure(figsize=(10, 6))

for file in plot_files:
    
    file_path = file
    
    # load data
    data = np.loadtxt(file_path)
    time = data[:, 0]
    signal = data[:, 1]

    # remove mean
    signal = signal - np.mean(signal)

    # sampling frequency
    dt = time[1] - time[0]
    fs = 1 / dt

    # FFT
    fft_vals = np.fft.fft(signal)
    amp = np.abs(fft_vals)

    # take only positive frequencies
    amp = amp[:len(amp)//2]

    # cumulative energy
    cum_energy = np.cumsum(amp**2)
    cum_energy = cum_energy / cum_energy[-1]   # normalize

    # frequency axis
    freq = np.fft.fftfreq(len(signal), d=dt)
    freq = freq[:len(freq)//2]

    # normalized fuel ratio
    fuel_val = float(file.replace(".txt", ""))
    phi_norm = fuel_val / phi_rbo

    # plot
    plt.plot(freq, cum_energy, label=f"$\\Phi/\\Phi_{{RBO}}$ = {phi_norm:.3f}")

# formatting
plt.xlabel("Frequency (Hz)")
plt.ylabel("ε(fi)")
plt.xlim(0, 100)   # same low freq focus
plt.ylim(0, 1)
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig("Figure_6_RBO_CumulativeEnergy_Y_Axis_Changed1.png", dpi=300)
plt.show()