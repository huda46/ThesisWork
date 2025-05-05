import random
import time
import psutil
import tracemalloc

def miller_rabin_test(n, k=40):
    """Return True if n is probably prime, False if composite."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^s * t
    s, t = 0, n - 1
    while t % 2 == 0:
        t //= 2
        s += 1

    # Perform k iterations of the test
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, t, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Composite
    return True  # Probably Prime

def generate_large_prime(bits, k=40):
    """Generate a large prime number using Miller-Rabin primality test."""
    while True:
        candidate = random.getrandbits(bits) | 1  # Ensure the number is odd
        if miller_rabin_test(candidate, k):
            return candidate

prime_512 = generate_large_prime(512)
print(f"Generated 512-bit prime: {prime_512}")

# def measure_memory_time(func, *args):
#     """Measure memory and time usage of a function."""
#     tracemalloc.start()
#     start_time = time.perf_counter()
#     start_mem = psutil.Process().memory_info().rss

#     result = func(*args)

#     end_time = time.perf_counter()
#     peak_mem = tracemalloc.get_traced_memory()[1]
#     tracemalloc.stop()

#     time_taken = end_time - start_time
#     memory_used = peak_mem / (1024 * 1024)  # Convert bytes to MB

#     return result, time_taken, memory_used

# # Example Usage:
# prime_512, time_taken, memory_used = measure_memory_time(generate_large_prime, 4096)

# print(f"Generated 512-bit prime: {prime_512}")
# print(f"Time taken: {time_taken:.6f} seconds | Memory used: {memory_used:.6f} MB")
