import sympy
import random
import math

# Step 1: Generate a small Multiprime RSA Key (for testing)
def generate_multiprime_rsa_key(bits=40):
    p = sympy.randprime(2**(bits-1), 2**bits)
    q = sympy.randprime(2**(bits-1), 2**bits)
    r = sympy.randprime(2**(bits-1), 2**bits)
    N = p * q * r
    phi_N = (p-1) * (q-1) * (r-1)
    
    # Choose a small public exponent e (typically 65537 in real RSA)
    e = 65537
    d = pow(e, -1, phi_N)  # Compute modular inverse of e mod phi(N)
    
    return (p, q, r, N, e, d)

# Step 2: Implement Pollard's Rho Factorization Algorithm
def pollards_rho(N):
    """ Pollard's Rho algorithm to find a nontrivial factor of N """
    if N % 2 == 0:
        return 2
    x = random.randint(2, N - 1)
    y = x
    c = random.randint(1, N - 1)
    d = 1

    def f(x):  # Polynomial function
        return (x*x + c) % N

    while d == 1:
        x = f(x)
        y = f(f(y))
        d = math.gcd(abs(x - y), N)
        if d == N:  # Failure case, restart with new parameters
            return None
    return d

# Step 3: Factorize a Number using Pollard’s Rho
def factorize_N(N):
    factors = []
    while N > 1:
        if sympy.isprime(N):  # If N is prime, stop
            factors.append(N)
            break
        factor = pollards_rho(N)
        if factor is None:
            break  # Give up if Pollard's fails (would need QS or GNFS)
        factors.append(factor)
        N //= factor
    return factors

# Step 4: Compute the Private Key from Factored Primes
def compute_private_key_from_factors(factors, e):
    """ Compute the private exponent d given the prime factors and e """
    phi_N = 1
    for prime in factors:
        phi_N *= (prime - 1)
    
    d_recovered = pow(e, -1, phi_N)  # Compute modular inverse of e mod phi(N)
    return d_recovered

# Generate RSA Key
p, q, r, N, e, d = generate_multiprime_rsa_key()

# Perform Factorization Attack
factored_primes = factorize_N(N)

# Compute Private Key from the factored primes
d_recovered = compute_private_key_from_factors(factored_primes, e) if len(factored_primes) >= 3 else None

# Display Results
print("Generated Primes:", p, q, r)
print("Modulus N:", N)
print("Factorized Primes:", factored_primes)
print("Recovered Private Key d:", d_recovered)