"""
this file is to simulate autocorrelation for RBO
the graph describes temporal behaviour of the signal

updated:
--> using Excel CORREL style (pearson correlation)
--> using short segment (2 sec)
--> removed unstable high lag region
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
    
    data = np.loadtxt(file_path)
    time = data[:, 0]
    signal = data[:, 1]

    # sampling frequency
    fs = 1 / (time[1] - time[0])

    # use only first 2 seconds
    signal = signal[:int(2 * fs)]

    # autocorrelation
    acf = []

    max_lag = 15
    min_points = 50

    for k in range(max_lag + 1):

        if k == 0:
            x1 = signal
            x2 = signal
        else:
            x1 = signal[:-k]
            x2 = signal[k:]

        if len(x1) < min_points:
            break

        r = np.corrcoef(x1, x2)[0, 1]
        acf.append(r)

    acf = np.array(acf)
    acf = np.nan_to_num(acf)

    lag = np.arange(len(acf))

    fuel_val = float(file.replace(".txt", ""))
    phi_norm = fuel_val / phi_rbo

    plt.plot(lag, acf, label=f"$\\Phi/\\Phi_{{RBO}}$ = {phi_norm:.3f}")

plt.xlabel("Lag")
plt.ylabel("Autocorrelation Function")

plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig("Figure_RBO_Autocorrelation.png", dpi=300)
plt.show()