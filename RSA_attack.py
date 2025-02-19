import random
from sympy import isprime, gcd, mod_inverse


#Generate small RSA key with waek primality test
def weak_key_gen():
    while True:
        p = random.randint(1000, 5000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000)
        q = random.randint(1000, 5000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000)
        if isprime(p) and isprime(q):
            break

    N = p * q
    phi = (p-1) * (q-1)
    e = 65537
    d = mod_inverse(e, phi)

    return (e, N), (d, N), (p, q)


#RSA Encryption
def encrypt_rsa(message, pub_key):
    e, N = pub_key
    return pow(message, e, N)

#RSA Decryption
def decrypt_rsa(message, priv_key):
    d, N = priv_key
    return pow(message, d, N)

# Attacker´s approach: Factorize N to find private key
def rsa_factor_attack(N):
    for i in range(2, int(N**0.5) + 1):
        if N % i == 0:
            return i, N // i 
    return None, None

# attack simulation
pub_key, priv_key, (p, q) = weak_key_gen()
N = pub_key[1]

#Attacker attempts to factorize N
factored_p, factored_q = rsa_factor_attack(N)

print(f"Genera Wear RSA modulus N: {N}")
print(f"Original Primes: p={p}, q={q}")
print(f"Attacker Factorized N: p={factored_p}, q={factored_q}")

# If factorization succeeds, attacker can compute the private key
if factored_p and factored_q:
    phi = (factored_p - 1) * (factored_q - 1)
    d_cracked = mod_inverse(65537, phi)
    print(f"Cracked Private Key: {d_cracked}")