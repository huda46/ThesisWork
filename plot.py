import time
import random
import matplotlib.pyplot as plt
from Trial_division import *
# Define algorithms
algorithms = {
    "Trial Division": Trial_division,
    "Fermat": lambda n: fermat_primality_test(n, 5),  # 5 iterations
    "Miller-Rabin": lambda n: miller_rabin_test(n, 5),  # 5 iterations
    "Solovay-Strassen": lambda n: solovay_strassen_test(n, 5),  # 5 iterations
    "AKS": aks_primality_test
}

# Input sizes and generated numbers
input_sizes = [2, 3, 4, 5]  # Number of digits
test_numbers = [random.randint(10**(d-1), 10**d - 1) for d in input_sizes]

# Measure execution times
execution_times = {algo: [] for algo in algorithms}
for num in test_numbers:
    for algo_name, algo_func in algorithms.items():
        start_time = time.perf_counter()
        algo_func(num)
        end_time = time.perf_counter()
        execution_times[algo_name].append(end_time - start_time)

# Plot the results
plt.figure(figsize=(10, 6))
for algo_name, times in execution_times.items():
    plt.plot(input_sizes, times, marker='o', label=algo_name)

# Add labels, legend, and title
plt.xlabel("Input Size (Number of Digits)", fontsize=12)
plt.ylabel("Execution Time (Seconds)", fontsize=12)
plt.title("Runtime Comparison of Primality Testing Algorithms", fontsize=14)
plt.legend(fontsize=10)
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()
