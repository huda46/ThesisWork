from sympy import nextprime, factorint
import random
import os

# Create ASN.1 Sequence for DH parameters
from pyasn1.type.univ import Integer, Sequence
from pyasn1.codec.der.encoder import encode

def generate_b_smooth_prime(bits=256, B=None):
    """
    Generate a prime where (p-1) is B-smooth.
    Ensures that all factors of (p-1) are ≤ B.
    """
    # If B is not provided, randomly choose a smoothness bound
    if B is None:
        B = random.randint(30, 100)  # Choose a random B within a reasonable range

    # Generate a list of small primes ≤ B
    small_primes = [p for p in range(2, B+1) if all(p % d != 0 for d in range(2, int(p**0.5)+1))]

    while True:
        p_minus_1 = 1  # Start constructing (p-1)

        # Keep multiplying by small primes
        while p_minus_1.bit_length() < bits - 1:
            factor = random.choice(small_primes)  # Always choose from small primes ≤ B
            p_minus_1 *= factor  # Multiply

        # Ensure that (p-1) contains only small primes ≤ B
        if max(factorint(p_minus_1).keys()) > B:
            continue  # Reject and try again

        # Ensure p is prime by finding the next prime after (p-1) + 1
        p = nextprime(p_minus_1 + 1)

        # Ensure p has the correct bit length
        if p.bit_length() == bits:
            return p, B  # Return both the prime and its B-smoothness bound

# Generate one smoothness value B to use for both p-1 and q-1
p, B = generate_b_smooth_prime(256)  # Get first prime and its smoothness bound
q, _ = generate_b_smooth_prime(256, B)  # Ensure q-1 has the same B

n = p * q  # Composite modulus

# Save p, q, and n for later use
with open("dh_values.txt", "w") as f:
    f.write(f"{p}\n{q}\n{n}\n")

print(f"✅ Saved backdoored p, q, n to `dh_values.txt`.")
print(f"Using smoothness bound B = {B}")


# Print values for verification
print(f"Generated p: {p} (Bits: {p.bit_length()})")
print(f"Generated q: {q} (Bits: {q.bit_length()})")
print(f"Composite modulus n: {n} (Bits: {n.bit_length()})")


# Convert n to exactly 64 bytes
n_bytes = n.to_bytes(64, byteorder="big")
# Encoding the DH parameters in ASN.1 format
print("\nEncoding DH parameters in ASN.1 format...")

g = 2  # Standard DH generator

dh_params = Sequence()
dh_params.setComponentByPosition(0, Integer(int.from_bytes(n_bytes, "big")))  # Replace prime P with backdoored modulus
dh_params.setComponentByPosition(1, Integer(g))  # Generator G

# Encode in DER format
der_encoded = encode(dh_params)

# Save the DER file
with open("backdoored_dhparams.der", "wb") as f:
    f.write(der_encoded)

print("✅ Successfully generated `backdoored_dhparams.der` with correct ASN.1 encoding!")


