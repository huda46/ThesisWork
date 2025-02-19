import math
import random
import time
import psutil
import tracemalloc
from gmpy2 import powmod, jacobi
from math import gcd, log, isqrt
from random import randint
from sympy import mod_inverse, isprime, symbols, expand, Mod

from math import gcd, isqrt, log, ceil
from sympy import symbols, Poly
from testEC import ecpp_certificate

# Trial division algorithm
def Trial_division(n):
    """Return True if n is prime, False if composite, ignoring small corner cases."""
    if n % 2 == 0 or n % 3 == 0:
        return False
    a = math.isqrt(n)
    for i in range(5, a + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

def fermat_primality_test(n, k):
    """Return True if n is probably prime, False if composite."""
    if n <= 1:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    for _ in range(k):
        # Choose a random base `a` coprime to `n`
        while True:
            a = random.randint(2, n - 2)
            if gcd(a, n) == 1:  # Ensure `a` is coprime to `n`
                break
        
        # Perform modular exponentiation
        if pow(a, n - 1, n) != 1:
            return False

    return True


# Miller-Rabin primality test
def miller_rabin_test(n, k):
    """Return True if n is probably prime, False if composite, ignoring small corner cases."""
    if n % 2 == 0:
        return False

    s = 0
    t = n - 1
    while t % 2 == 0:
        t //= 2
        s += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        b = powmod(a, t, n)
        if b == 1 or b == n - 1:
            continue
        for _ in range(s - 1):
            b = powmod(b, 2, n)
            if b == n - 1:
                break
        else:
            return False
    return True

# Solovay-Strassen primality test
def solovay_strassen_test(n, k):
    """Return True if n is probably prime, False if composite."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        gcd = math.gcd(a, n)
        if gcd > 1:
            return False  # Composite

        # Compute Jacobi symbol
        jacobi_symbol = jacobi(a, n)

        # Modular exponentiation and comparison
        mod_exp = powmod(a, (n - 1) // 2, n)
        if mod_exp != jacobi_symbol % n:
            return False
    return True

# AKS Algorithm
# first check if n is perfect power
def is_perfect_power(n):
    """
    Checks if n is a perfect power (n = a^b for a > 1 and b > 1).
    """
    for b in range(2, isqrt(n) + 2):
        a = round(n ** (1 / b))
        if a ** b == n:
            return True
    return False

def find_r(n):
    """
    Finds the smallest r such that the order of n modulo r is greater than log(n, 2)^2.
    """
    max_k = ceil(log(n, 2) ** 2)
    for r in range(2, n):
        order = 1
        while pow(n, order, r) != 1 and order <= max_k:
            order += 1
        if order > max_k:
            return r
    return n

def euler_totient(r):
    """
    Computes Euler's Totient function φ(r).
    """
    result = r
    p = 2
    while p * p <= r:
        if r % p == 0:
            while r % p == 0:
                r //= p
            result -= result // p
        p += 1
    if r > 1:
        result -= result // r
    return result

def poly_mod_exp(base, exp, mod_poly, modulus):
    """
    Modular exponentiation for polynomials.
    """
    result = Poly(1, symbols('x'), modulus=modulus)
    base = base % mod_poly
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod_poly
        base = (base * base) % mod_poly
        exp //= 2
    return result

def optimized_polynomial_mod_check(n, r):
    """
    Optimized polynomial congruence check:
    Verifies (x + a)^n ≡ x^n + a (mod x^r - 1, n) for 1 ≤ a ≤ √φ(r) log(n).
    """
    x = symbols('x')
    mod_poly = Poly(x ** r - 1, x, modulus=n)
    max_a = ceil(isqrt(euler_totient(r)) * log(n, 2))
    
    for a in range(1, max_a + 1):
        base = Poly(x + a, x, modulus=n)
        lhs = poly_mod_exp(base, n, mod_poly, n)
        rhs = Poly(x ** n + a, x, modulus=n) % mod_poly
        if lhs != rhs:
            return False
    return True

def aks_primality_test(n):
    """
    AKS primality test implementation.
    """
    if n < 2:
        return False
    
    # Step 1: Check if n is a perfect power
    if is_perfect_power(n):
        return False
    
    # Step 2: Find the smallest r
    r = find_r(n)
    
    # Step 3: Check for small prime factors
    for a in range(2, min(r + 1, n)):
        if n % a == 0 and n != a:
            return False
    
    # Step 4: Polynomial congruence check
    if n > r:
        if not optimized_polynomial_mod_check(n, r):
            return False
    
    # Step 5: If all checks pass, n is prime
    return True




def measure_memory_time(func, *args):
    """Measure memory and time usage of a function."""
    tracemalloc.start()
    start_time = time.perf_counter()
    start_mem = psutil.Process().memory_info().rss  # Corrected access to memory info

    result = func(*args)

    end_time = time.perf_counter()
    peak_mem = tracemalloc.get_traced_memory()[1]  # Corrected function call syntax
    tracemalloc.stop()

    time_taken = end_time - start_time
    memory_used = peak_mem / (1024 * 1024)  # Convert bytes to MB

    return bool(result), time_taken, memory_used



def compare_algorithms(n, k, a, b, m, q):
    """Compare the execution time of Trial Division, Fermat Primality Test, Miller-Rabin Test, AKS. ECPP and Solovay-Strassen Test."""
    print("Calculations may take some time. Please wait...\n")

    # Timing Trial Division
    # print("Running Trial Division...")
    # trial_result, trial_time, trial_mem = measure_memory_time(Trial_division, n)
    # print(f"Trial Division: {'Prime' if trial_result else 'Composite'}")
    # print(f"Time taken: {trial_time:.9f} seconds | Memory used: {trial_mem:.6f} MB\n")    
    # print("Trial Division completed.\n")

    # Timing Fermat Primality Test
    print("Running Fermat Primality Test...")
    fermat_result, fermat_time, fermat_mem = measure_memory_time(fermat_primality_test, n, k)
    print(f"Fermat Primality Test: {'Probably Prime' if fermat_result else 'Composite'}")
    print(f"Time taken: {fermat_time:.9f} seconds | Memory used: {fermat_mem:.6f} MB\n")    
    print("Fermat Primality Test completed.\n")

    # Timing Miller-Rabin Primality Test
    print("Running Miller-Rabin Primality Test...")
    miller_rabin_result, miller_rabin_time, miller_rabin_mem = measure_memory_time(miller_rabin_test, n, k)
    print(f"Miller-Rabin Primality Test: {'Probably Prime' if miller_rabin_result else 'Composite'}")
    print(f"Time taken: {miller_rabin_time:.9f} seconds | Memory used: {miller_rabin_mem:.6f} MB\n")    
    print("Miller-Rabin Primality Test completed.\n")

    # Timing Solovay-Strassen Test
    print("Running Solovay-Strassen Test...")
    solovay_strassen_result, solovay_strassen_time, solovay_strassen_mem = measure_memory_time(solovay_strassen_test, n, k)

    print(f"Solovay-Strassen Test: {'Probably Prime' if solovay_strassen_result else 'Composite'}")
    print(f"Time taken: {solovay_strassen_time:.9f} seconds | Memory used: {solovay_strassen_mem:.6f} MB\n")    
    print("Solovay-Strassen Test completed.\n")

    # ECPP Primality Test
    print("Running ECPP Test...")
    ecpp_result, ecpp_time, ecpp_mem = measure_memory_time(ecpp_certificate, n)
    print(f"ECPP Test: {'Prime' if ecpp_result else 'Composite'}")
    print(f"Time taken: {ecpp_time:.9f} seconds | Memory used: {ecpp_mem:.6f} MB\n")

    # Timing AKS
    print("Running AKS Test...")
    aks_result, aks_time, aks_mem = measure_memory_time(aks_primality_test, n)
    print(f"AKS Test: {'Prime' if aks_result else 'Composite'}")
    print(f"Time taken: {aks_time:.9f} seconds | Memory used: {aks_mem:.6f} MB\n")   
    print("AKS Test completed.\n")
 



