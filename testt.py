import logging
import os
import sys
from sage.all import RR, ZZ

# Importing necessary functions
from attacks.factorization import known_phi
from shared.small_roots import herrmann_may

def attack_multi_prime(N, e, factor_bit_length, factors, delta=0.25, m=1, t=None):
    """
    Recovers the prime factors if the private exponent is too small using the Boneh-Durfee attack.
    This method is adapted for a modulus consisting of multiple prime factors.
    
    :param N: the RSA modulus (product of multiple primes)
    :param e: the public exponent
    :param factor_bit_length: estimated bit length of the prime factors
    :param factors: the number of prime factors in the modulus
    :param delta: a predicted bound on the private exponent (d < N^delta) (default: 0.25)
    :param m: lattice parameter (default: 1)
    :param t: polynomial degree parameter (default: auto-calculated based on m)
    :return: a tuple containing the prime factors and the private exponent d, or None if the attack fails
    """
    x, y = ZZ["x", "y"].gens()
    A = N + 1  # Approximation for totient function
    f = x * (A + y) + 1  # Polynomial used for small roots attack

    # Setting bounds for small root attack
    X = int(RR(e) ** delta)
    Y = int(2 ** ((factors - 1) * factor_bit_length + 1))
    t = int((1 - 2 * delta) * m) if t is None else t
    
    logging.info(f"Trying m={m}, t={t} for multi-prime attack...")
    
    for x0, y0 in herrmann_may.modular_bivariate(f, e, m, t, X, Y):
        z = int(f(x0, y0))
        if z % e == 0:
            k = pow(x0, -1, e)
            s = (N + 1 + k) % e
            phi = N - s + 1  # Estimate phi(N) from small root solution
            factors = known_phi.factorize_multi_prime(N, phi)
            if factors:
                logging.info(f"Recovered factors: {factors}")
                
                # Compute private exponent d
                d = pow(e, -1, phi)
                logging.info(f"Recovered private exponent d: {d}")
                
                return factors, d
    
    return None
