import subprocess
import re
from sympy.ntheory.residue_ntheory import discrete_log
from sympy.ntheory.modular import crt
from sympy import factorint

def extract_public_key():
    """Extract DH public key (y_A) from OpenSSL and convert to an integer."""
    openssl_cmd = "openssl pkey -pubin -in NOBUS_DH_attack/public_key.pem -text -noout"
    output = subprocess.run(openssl_cmd, shell=True, capture_output=True, text=True).stdout
    hex_matches = re.findall(r'([0-9A-Fa-f:]+)', output)
    hex_y_A = "".join(hex_matches[1:]).replace(":", "")
    return int(hex_y_A, 16)

# Extract public key
y_A = extract_public_key()
print(f"✅ Extracted y_A: {y_A}")
g = 2 
# Load p and q from the saved file
with open("NOBUS_DH_attack/dh_values.txt", "r") as f:
    p = int(f.readline().strip()) 
    q = int(f.readline().strip())
    
print(f"p: {p} extracted from file")
print(f"q: {q} extracted from file")
print(f"g: {g}")


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

# Solve for private key
x_p = pohlig_hellman(y_A % p, g, p)
x_q = pohlig_hellman(y_A % q, g, q)

x_recovered, _ = crt([p-1, q-1], [x_p, x_q])
print(f"✅ Recovered Private Key x_A: {x_recovered}")
