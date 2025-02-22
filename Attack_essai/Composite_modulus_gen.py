from sympy import nextprime, factorint
import random
import os
import subprocess
from pyasn1.type.univ import Integer, Sequence
from pyasn1.codec.der.encoder import encode

def generate_exact_b_smooth_number(bits=32, B=10):
    """Generate a B-smooth number S (all factors ≤ B)."""
    
    # Generate a list of small primes ≤ B
    small_primes = [p for p in range(2, B+1) if all(p % d != 0 for d in range(2, int(p**0.5)+1))]
    
    S = 1  # Start constructing the B-smooth number
    
    while S.bit_length() < bits - 1:  # Ensure it’s close to the target size
        factor = random.choice(small_primes)  # Always pick factors ≤ B
        S *= factor

    return S  # Return the B-smooth number

# Step 1: Choose a smoothness bound B (fixed for both p and q)
B = random.randint(5, 10)  # Choose a random B (or set manually)

# Step 2: Generate a B-smooth number S
S = generate_exact_b_smooth_number(32, B)

# Step 3: Ensure p-1 = S and q-1 = S by finding primes p and q
p = nextprime(S + 1)
q = nextprime(S + 2)

n = p * q  # Composite modulus
g = 2  # Generator

os.makedirs("Attack_essai", exist_ok=True)

# Save values for later use
with open("Attack_essai/dh_values.txt", "w") as f:
    f.write(f"{p}\n{q}\n{n}\n")

print(f"✅ Saved p, q, n to `dh_values.txt`.")
print(f"Generated p: {p} (Bits: {p.bit_length()})")
print(f"Generated q: {q} (Bits: {q.bit_length()})")
print(f"Composite modulus n: {n} (Bits: {n.bit_length()})")
print(f"Using smoothness bound B = {B}")
print(f"Factorization of p-1 (Should match q-1): {factorint(p - 1)}")
print(f"Factorization of q-1 (Should match p-1): {factorint(q - 1)}")

# Create ASN.1 Sequence for DH parameters
dh_params = Sequence()
dh_params.setComponentByPosition(0, Integer(n))  # Backdoored modulus
dh_params.setComponentByPosition(1, Integer(g))  # Generator G

# Encode in DER format
der_encoded = encode(dh_params)
with open("Attack_essai/backdoored_dhparams.der", "wb") as f:
    f.write(der_encoded)

print("✅ Successfully generated `backdoored_dhparams.der`!")

# Convert to PEM format using OpenSSL
subprocess.run(
    "openssl dhparam -inform DER -in Attack_essai/backdoored_dhparams.der -out Attack_essai/backdoored_dhparams.pem",
    shell=True
)

print("✅ Converted `backdoored_dhparams.der` to PEM format!")

# Generate OpenSSL DH key pair
subprocess.run(
    "openssl genpkey -paramfile Attack_essai/backdoored_dhparams.pem -out Attack_essai/private_key.pem",
    shell=True
)
subprocess.run(
    "openssl pkey -in Attack_essai/private_key.pem -pubout -out Attack_essai/public_key.pem",
    shell=True
)

print("✅ Generated OpenSSL DH key pair!")
