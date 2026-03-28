"""
this file is to simulate the autocorrelation for RBO
the graph describes temporal behaviour of the signal

The fig includes:

Autocorrelation decay for three fuel conditions:
1. Low fuel (stable)
2. Mid fuel
3. Near RBO

We find:
--> correlation reduces as lag increases
--> behaviour changes as we approach RBO
"""

"""
same method as LBO.
we compute normalized autocorrelation and plot decay
over a short lag window.
"""

# imports
import numpy as np
import matplotlib.pyplot as plt
import os

# plot settings for larger fonts
plt.rcParams.update({
    "font.size": 26,
    "axes.labelsize": 26,
    "xtick.labelsize": 26,
    "ytick.labelsize": 26,
    "axes.titlesize": 26
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

    # autocorrelation
    corr = np.correlate(signal, signal, mode='full')
    center = corr.size // 2

    # take only positive lags
    corr = corr[center:]
    corr = corr / corr[0]

    # time axis (ms)
    lag = (np.arange(len(corr)) / fs) * 1000

    # take only first 100 ms (same as LBO)
    max_lag = int(0.1 * fs)

    corr = corr[:max_lag]
    lag = lag[:max_lag]

    # normalized fuel ratio
    fuel_val = float(file.replace(".txt", ""))
    phi_norm = fuel_val / phi_rbo

    # plot
    plt.plot(lag, corr, label=f"$\\Phi/\\Phi_{{RBO}}$ = {phi_norm:.3f}")

# formatting
plt.xlabel("Lag Time (ms)")
plt.ylabel("Autocorrelation Coefficient")
plt.axhline(0, color='black', linewidth=1, alpha=0.5)
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig("Figure_5_RBO_Autocorrelation.png", dpi=300)
plt.show()