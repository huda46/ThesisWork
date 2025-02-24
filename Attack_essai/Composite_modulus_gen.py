from sympy import nextprime, factorint
import random
import os
import subprocess
from pyasn1.type.univ import Integer, Sequence
from pyasn1.codec.der.encoder import encode

def generate_b_smooth_prime(bits=32, B=100):
    """Generate a small prime where (p-1) is B-smooth."""
    small_primes = [p for p in range(2, B+1) if all(p % d != 0 for d in range(2, int(p**0.5)+1))]
    print(f"{small_primes}")
    while True:
        p_minus_1 = 1
        while p_minus_1.bit_length() < bits - 1:
            factor = random.choice(small_primes)
            p_minus_1 *= factor

        p = nextprime(p_minus_1 + 1)
        if p.bit_length() == bits:
            return p

# Generate small backdoored primes p and q
p = generate_b_smooth_prime(32)
q = generate_b_smooth_prime(32)
n = p * q  # Composite modulus
g = 2  # Generator


# Save values for later use
with open("dh_values.txt", "w") as f:
    f.write(f"{p}\n{q}\n{n}\n")

print(f"✅ Saved p, q, n to `dh_values.txt`.")
print(f"Generated p: {p} (Bits: {p.bit_length()})")
print(f"Generated q: {q} (Bits: {q.bit_length()})")
print(f"Composite modulus n: {n} (Bits: {n.bit_length()})")
print(f"Factorization of p-1: {factorint(p - 1)}")
print(f"Factorization of q-1: {factorint(q - 1)}")

# Create ASN.1 Sequence for DH parameters
dh_params = Sequence()
dh_params.setComponentByPosition(0, Integer(n))  # Backdoored modulus
dh_params.setComponentByPosition(1, Integer(g))  # Generator G

# Encode in DER format
der_encoded = encode(dh_params)
with open("backdoored_dhparams.der", "wb") as f:
    f.write(der_encoded)

print("✅ Successfully generated `backdoored_dhparams.der`!")

# Convert to PEM format using OpenSSL
subprocess.run(
    "openssl dhparam -inform DER -in backdoored_dhparams.der -out backdoored_dhparams.pem",
    shell=True
)

print("✅ Converted `backdoored_dhparams.der` to PEM format!")

# Generate OpenSSL DH key pair
subprocess.run(
    "openssl genpkey -paramfile backdoored_dhparams.pem -out private_key.pem",
    shell=True
)
subprocess.run(
    "openssl pkey -in private_key.pem -pubout -out public_key.pem",
    shell=True
)

print("✅ Generated OpenSSL DH key pair!")
