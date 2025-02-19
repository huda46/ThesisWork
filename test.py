from math import gcd, isqrt, log, ceil
from sympy import symbols, Poly

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

# Test the function with a large number
n = 101
print(f"{n} is prime: {aks_primality_test(n)}")
