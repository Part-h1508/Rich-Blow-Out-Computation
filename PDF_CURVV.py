"""
this file is to simulate the PDF curve for RBO
the graph describes statistical behaviour of the signal

The fig includes:

PDF plots for three fuel conditions:
1. Low fuel (stable)
2. Mid fuel (transition)
3. Near RBO

We find:
--> distribution changes as we approach RBO
--> deviation from gaussian behaviour appears
"""

"""
same method as before.
we normalize the signal and plot histogram
along with gaussian curve for comparison.
"""

# imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
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

# choose 3 cases
plot_files = ["5.0.txt", "5.8.txt", "6.3.txt"]

plt.figure(figsize=(14, 5))

for i, file in enumerate(plot_files):
    
    file_path = file
    
    # load data
    data = np.loadtxt(file_path)
    signal = data[:, 1]

    # normalize signal
    signal_norm = (signal - np.mean(signal)) / np.std(signal)

    # subplot
    plt.subplot(1, 3, i+1)

    # histogram
    plt.hist(signal_norm, bins=100, density=True,
             alpha=0.6, color='blue')

    # gaussian curve
    x = np.linspace(-4, 4, 100)
    plt.plot(x, norm.pdf(x, 0, 1), 'r--', linewidth=2)

    # labels
    fuel_val = float(file.replace(".txt", ""))
    phi_norm = fuel_val / phi_rbo

    plt.title(f"$\\Phi/\\Phi_{{RBO}}$ = {phi_norm:.3f}")
    plt.xlabel("Normalized amplitude")
    plt.ylim(0, 0.6)

    plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("Figure_4_RBO_PDF.png", dpi=300)
plt.show()