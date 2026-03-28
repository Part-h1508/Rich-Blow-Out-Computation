"""
this file is to simulate the NRMS variation for RBO
the graph describes fluctuation intensity of the signal

The fig includes:

NRMS plotted against normalized fuel ratio (Φ/Φ_RBO)

We find:
--> NRMS remains low for stable conditions
--> as we approach RBO, NRMS increases
--> shows transition in combustion behaviour
"""

"""
same approach as LBO.
we calculate NRMS = std / mean for each signal
and plot it against normalized fuel ratio.
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

files = sorted([f for f in os.listdir('.') if f.endswith('.txt')])

phi_norm_list = []
nrms_list = []

for file in files:
    
    if not file.endswith(".txt"):
        continue

    file_path = file
    
    # load data
    data = np.loadtxt(file_path)
    signal = data[:, 1]

    # NRMS calculation
    mean_val = np.mean(signal)
    std_val = np.std(signal)

    nrms = std_val / mean_val

    # normalized fuel ratio
    fuel_val = float(file.replace(".txt", ""))
    phi_norm = fuel_val / phi_rbo

    phi_norm_list.append(phi_norm)
    nrms_list.append(nrms)

# sort (important)
phi_norm_list = np.array(phi_norm_list)
nrms_list = np.array(nrms_list)

sorted_indices = np.argsort(phi_norm_list)

phi_norm_list = phi_norm_list[sorted_indices]
nrms_list = nrms_list[sorted_indices]

# plotting
plt.figure(figsize=(8, 6))
plt.plot(phi_norm_list, nrms_list, marker='o', color='blue')

# threshold line (same as LBO reference)
plt.axhline(y=0.3, linestyle='--', color='black')

# RBO line
plt.axvline(x=0.9576, linestyle='--', color='red')

# labels
plt.xlabel("Normalized Fuel Ratio ($\\Phi/\\Phi_{{RBO}}$)") 
plt.ylabel("NRMS")


plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("Figure_3_RBO_NRMS.png", dpi=300)
plt.show()