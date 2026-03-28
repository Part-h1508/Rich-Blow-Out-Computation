"""
this file is to simulate the 1st figure (RBO)
the graph describes physical behaviour of the raw signals

The fig includes:

Three subplots showing time series evolution:
1. Low fuel flow (far from RBO)
2. Mid fuel flow (approaching RBO)
3. Highest fuel flow (near RBO)

We find:
raw signal --> stable oscillations at low fuel
--> increased fluctuations at mid fuel
--> strong intermittency near RBO
"""

# imports
import numpy as np
import matplotlib.pyplot as plt
import os

# variables
phi_rbo = 6.3   # given

# manually choose files (adjust based on your data)
# example: lowest, middle, highest
plot_files = ["5.0.txt", "5.8.txt", "6.3.txt"]

fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

for i, file in enumerate(plot_files):
    
    file_path = file
    
    # load data
    data = np.loadtxt(file_path)
    time = data[:, 0]
    signal = data[:, 1]
    
    # normalize time to start from 0
    time = time - time[0]
    
    # get fuel value from filename
    fuel = float(file.replace(".txt", ""))
    phi_norm = fuel / phi_rbo
    
    # plot full 20s signal
    axes[i].plot(time, signal, color="#ff0000", linewidth=0.6)
    
    # title with normalized value
    axes[i].set_title(f"Φ / Φ_RBO = {phi_norm:.3f}")
    axes[i].set_ylabel("Amplitude")
    axes[i].grid(True, alpha=0.3)

plt.xlabel("Time (s)")
plt.tight_layout()
plt.savefig("Figure_1_RBO_TimeSeries.png", dpi=300)
plt.show()