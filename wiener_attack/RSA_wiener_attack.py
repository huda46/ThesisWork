import random
from sympy import nextprime
from fractions import Fraction
from sympy import continued_fraction, continued_fraction_convergents
from math import isqrt, sqrt, gcd

def generate_multiprime_rsa_params(bits=128):
    """
    Generate a multi-prime RSA key where N = p * q * r.
    Ensures d satisfies d < N^(1/6) / sqrt(10).
    """
    p = nextprime(random.getrandbits(bits))
    q = nextprime(random.getrandbits(bits))
    #r = nextprime(random.getrandbits(bits))

    N = p * q #* r  
    phi_N = (p - 1) * (q - 1) #* (r - 1)

    # Calculate the limit for Wiener's attack
    d_limit = int((N ** (1/4)) / sqrt(6))

    while True:
        d = random.randint(max(1000, d_limit // 10), d_limit)  # Ensure d is not trivially small
        if gcd(d, phi_N) == 1:  
            break
    

    # Compute e as modular inverse of d modulo phi(N)
    e = pow(d, -1, phi_N)

    print(f"Generated Multi-Prime RSA parameters:\nN = {N}\ne = {e}\nd = {d}\nd_limit = {d_limit}")
    return N, e, d

def wiener_attack(N, e):
    """
    Wiener's attack on RSA using continued fraction expansion.
    """
    cf_expansion = continued_fraction(Fraction(e, N))
    convergents = continued_fraction_convergents(cf_expansion)

    for conv in convergents:
        k, d = conv.numerator, conv.denominator
        
        if k == 0:
            continue

        # Check if d is a possible private exponent
        phi_N = (e * d - 1) // k
        if (e * d - 1) % k == 0:
            # Solve for phi(N)
            b = N - phi_N + 1
            delta = b**2 - 4*N

            if delta >= 0:
                sqrt_delta = isqrt(delta)
                if sqrt_delta * sqrt_delta == delta:
                    print(f"Private exponent recovered: d = {d}")
                    return d

    print("Attack failed: d is not sufficiently small.")
    return None

# Generate Multi-Prime RSA keys (N = p * q * r)
N, e, d = generate_multiprime_rsa_params()

# Test Wiener's attack
recovered_d = wiener_attack(N, e)

# Verify if attack succeeded
if recovered_d == d:
    print("Wiener's attack successfully recovered d!")
else:
    print("Wiener's attack failed.")
