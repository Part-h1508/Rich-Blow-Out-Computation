"""
this file is to simulate theta for RBO
theta represents normalized duration above threshold

we use amplitude-based threshold similar to LBO
"""

import numpy as np
import matplotlib.pyplot as plt
import os

folder_path = "."
phi_rbo = 6.3

files = sorted(os.listdir(folder_path))


theta_values = []
phi_norm_list = []

# get stable case (lowest fuel condition)
stable_file = "5.0.txt"

data_stable = np.loadtxt(os.path.join(folder_path, stable_file))
stable_signal = data_stable[:, 1]

# remove mean
stable_signal = stable_signal - np.mean(stable_signal)

for file in files:

    if not file.endswith(".txt"):
        continue

    file_path = os.path.join(folder_path, file)
    
    data = np.loadtxt(file_path)
    signal = data[:, 1]

    # remove mean
    signal = signal - np.mean(signal)

    # threshold (70% of max amplitude)
    threshold = 2 * np.std(stable_signal)

    # count exceedances
    count = np.sum(np.abs(signal) > threshold)
    theta = count / len(signal)

    # normalized fuel ratio
    fuel_val = float(file.replace(".txt", ""))
    phi_norm = fuel_val / phi_rbo

    theta_values.append(theta)
    phi_norm_list.append(phi_norm)

# sort
phi_norm_list = np.array(phi_norm_list)
theta_values = np.array(theta_values)

idx = np.argsort(phi_norm_list)

phi_norm_list = phi_norm_list[idx]
theta_values = theta_values[idx]

# plot
plt.figure(figsize=(8, 6))
plt.plot(phi_norm_list, theta_values, marker='o')

plt.xlabel("$\\Phi/\\Phi_{{RBO}}$")
plt.ylabel("$\\Theta$")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("Figure_RBO_theta.png", dpi=300)
plt.show()