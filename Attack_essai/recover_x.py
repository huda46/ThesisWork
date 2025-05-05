import subprocess
import re
import os
from sympy.ntheory.residue_ntheory import discrete_log
from sympy.ntheory.modular import crt
from sympy import factorint

def extract_public_key():
    """Extract the DH public key (y_A) from OpenSSL and convert it to an integer."""
    
    # Run OpenSSL command
    openssl_cmd = "openssl pkey -pubin -in public_key.pem -text -noout"
    result = subprocess.run(openssl_cmd, shell=True, capture_output=True, text=True)

    output = result.stdout.strip()

    # Handle OpenSSL errors
    if result.returncode != 0:
        print(f"❌ OpenSSL command failed: {result.stderr}")
        raise FileNotFoundError("❌ OpenSSL could not read `public_key.pem`. Ensure it exists and is valid.")

    if not output:
        raise ValueError("❌ OpenSSL output is empty! Ensure `public_key.pem` was generated correctly.")

    # Extract the public key (decimal format)
    match = re.search(r'public-key:\s+(\d+)', output)
    
    if not match:
        raise ValueError("❌ Could not extract DH public key. Ensure `public_key.pem` is valid.")

    # Convert public key to integer
    return int(match.group(1))

# Extract Alice's public key
try:
    y_A = extract_public_key()
    print(f"✅ Extracted Alice's public key: {y_A}")
except Exception as e:
    print(e)
    exit(1)

# Load p and q from saved file
with open("dh_values.txt", "r") as f:
    p = int(f.readline().strip()) 
    q = int(f.readline().strip())

g = 2  # Generator

print(f"Loaded values: p = {p}, q = {q}, g = {g}")
print(f"Factorization of p-1: {factorint(p - 1)}")
print(f"Factorization of q-1: {factorint(q - 1)}")

def pohlig_hellman(y, g, p):
    """Computes discrete log x in g^x ≡ y (mod p) using Pohlig-Hellman."""
    factors = factorint(p - 1)
    x_values, moduli = [], []

    for q, e in factors.items():
        q_exp = q ** e
        g_q = pow(g, (p-1) // q_exp, p)
        y_q = pow(y, (p-1) // q_exp, p)

        try:
            x_q = discrete_log(p, y_q, g_q, q_exp)
            x_values.append(x_q)
            moduli.append(q_exp)
        except ValueError:
            print(f"⚠️ Warning: Discrete log does not exist for factor {q_exp}")
            continue

    if not x_values:
        raise ValueError("Failed to compute discrete log for any factor!")

    return crt(moduli, x_values)[0]

# Recover Alice’s private key
try:
    x_p = pohlig_hellman(y_A % p, g, p)
    x_q = pohlig_hellman(y_A % q, g, q)
    x_recovered, _ = crt([p-1, q-1], [x_p, x_q])
    print(f"✅ Recovered Alice's Private Key: {x_recovered}")
except Exception as e:
    print(f"❌ Error in private key recovery: {e}")
