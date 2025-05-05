import matplotlib.pyplot as plt
import numpy as np

# Trimmed dataset up to 10^70 + 33
number_labels_trimmed = [
    "109", "1097", "10313", "100207",
    "10¹³+37", "10¹⁵+91",
    "10²⁰+151", "10⁵⁰+447", "10⁷⁰+33"
]
log_numbers_trimmed = [3, 4, 5, 6, 13, 15, 20, 50, 70]

# td_times_trimmed = [0.00057, 0.00033, 0.00042, 0.001214, 0.466195, 4.71225, None, None, None]
# ecpp_times_trimmed = [0.00151, 0.00506, 0.00937, 0.08568, 0.03188, 0.04838, 1.09796, 3.21926, 92.96664]
# aks_times_trimmed = [2.20514, 41.26039, 626.81946, None, None, None, None, None, None]

# # Replace None with np.nan
# td_times_trimmed = [np.nan if t is None else t for t in td_times_trimmed]
# aks_times_trimmed = [np.nan if t is None else t for t in aks_times_trimmed]

# # Create the plot
# plt.figure(figsize=(14, 6))
# plt.plot(log_numbers_trimmed, td_times_trimmed, label="Trial Division", marker='s')
# plt.plot(log_numbers_trimmed, ecpp_times_trimmed, label="ECPP", marker='o')
# plt.plot(log_numbers_trimmed, aks_times_trimmed, label="AKS", marker='^')

# plt.yscale("log")
# plt.xticks(log_numbers_trimmed, number_labels_trimmed, rotation=60, ha='right')
# plt.ylabel("Computation Time (sec)")
# plt.xlabel("Number Tested", labelpad=10)
# plt.title("Computation Time up to $10^{70} + 33$")
# plt.legend()
# plt.grid(True)

# # Save to PNG
# plt.tight_layout()
# plt.savefig("primality_test_comparison_up_to_10e70.png")
# plt.show()

import matplotlib.pyplot as plt

# Labels and log-scaled x-axis positions
number_labels = [
    "109", "1097", "10313", "100207",
    "10¹³+37", "10¹⁵+91", "10²⁰+151",
    "10⁵⁰+447", "10⁷⁰+33", "10¹⁰⁰+949",
    "10²⁰⁰+1849", "10⁵⁰⁰+3229", "10¹⁰⁰⁰+4351"
]
log_numbers = [3, 4, 5, 6, 13, 15, 20, 50, 70, 100, 200, 500, 1000]

# Times for k = 40 and 80
fermat_40 = [0.00027, 0.00047, 0.0008, 0.00095, 0.00102, 0.0034, 0.0043, 0.0151, 0.0165, 0.0213, 0.049, 0.2357, 1.481]
fermat_80 = [0.00032, 0.00055, 0.00059, 0.00128, 0.00338, 0.00412, 0.0054, 0.0153, 0.02197, 0.03734, 0.11632, 0.9519, 6.45708]
mr_40 = [0.000136, 0.00050, 0.00033, 0.00036, 0.00021, 0.00023, 0.00055, 0.00137, 0.0014, 0.00125, 0.0027, 0.0365, 0.2022]
mr_80 = [0.00026, 0.00045, 0.00034, 0.00083, 0.00038, 0.00086, 0.00048, 0.00104, 0.00165, 0.00303, 0.01218, 0.12601, 0.87857]
ss_40 = [0.000126, 0.00038, 0.00047, 0.00038, 0.00018, 0.00020, 0.00079, 0.00118, 0.00109, 0.0013, 0.0028, 0.0377, 0.2046]
ss_80 = [0.00022, 0.00035, 0.00032, 0.001834, 0.00040, 0.00048, 0.00055, 0.00121, 0.00169, 0.00431, 0.01337, 0.12809, 0.81624]

# Trim up to 10^70 + 33
trim_index = number_labels.index("10⁷⁰+33") + 1
number_labels_trimmed = number_labels[:trim_index]
log_numbers_trimmed = log_numbers[:trim_index]
fermat_40_trim = fermat_40[:trim_index]
fermat_80_trim = fermat_80[:trim_index]
mr_40_trim = mr_40[:trim_index]
mr_80_trim = mr_80[:trim_index]
ss_40_trim = ss_40[:trim_index]
ss_80_trim = ss_80[:trim_index]

# Plotting
plt.figure(figsize=(14, 7))
plt.plot(log_numbers_trimmed, fermat_40_trim, label="Fermat k=40", marker='o')
plt.plot(log_numbers_trimmed, fermat_80_trim, label="Fermat k=80", marker='o')
plt.plot(log_numbers_trimmed, mr_40_trim, label="Miller-Rabin k=40", marker='s')
plt.plot(log_numbers_trimmed, mr_80_trim, label="Miller-Rabin k=80", marker='s')
plt.plot(log_numbers_trimmed, ss_40_trim, label="Solovay-Strassen k=40", marker='^')
plt.plot(log_numbers_trimmed, ss_80_trim, label="Solovay-Strassen k=80", marker='^')

plt.yscale("log")
plt.xticks(log_numbers_trimmed, number_labels_trimmed, rotation=60, ha='right')
plt.ylabel("Computation Time (sec)")
plt.xlabel("Number Tested", labelpad=10)
plt.title("Probabilistic Primality Tests")
plt.legend()
plt.grid(True)

# Save and show
plt.tight_layout()
plt.savefig("probabilistic_tests.png")
plt.show()
