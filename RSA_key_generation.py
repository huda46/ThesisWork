import random
from sympy import mod_inverse
from Trial_division import *
def generate_large_prime(bits, test_function, iterations=10):
    """Generate a large prime number using a specified primality test."""
    while True:
        candidate = random.getrandbits(bits) | 1  # Ensure it's odd
        if test_function(candidate, iterations):
            return candidate

# Example: RSA Key Generation
bits = 1024  # Key size
p = generate_large_prime(bits, miller_rabin_test)  # Using Miller-Rabin
q = generate_large_prime(bits, miller_rabin_test)
n = p * q
phi = (p - 1) * (q - 1)
e = 65537  # Common public exponent
d = mod_inverse(e, phi)
print(f"p={p} q={q}")
print(f"Public Key: (n={n}, e={e})")
print(f"Private Key: (d={d})")

