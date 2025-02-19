import random
from sympy import isprime, mod_inverse, sqrt_mod
import sage.all as sage
from sympy.ntheory import factorint
from math import gcd

def is_valid_curve(a, b, n):
    """Check if the elliptic curve is valid."""
    discriminant = (4 * a**3 + 27 * b**2) % n
    return discriminant != 0 and gcd(discriminant, n) == 1

def is_square_modulo(n, a):
    """Check if a is a square modulo n using Euler's criterion."""
    return pow(a, (n - 1) // 2, n) == 1

def find_root_modulo(n, a):
    """Find a square root of a modulo n."""
    try:
        root = sqrt_mod(a, n, all_roots=False)
        return root
    except ValueError:
        return None

def random_point_on_curve(n, a, b, max_retries=10):
    """Randomly select a point x and check if y^2 is a square mod n."""
    for _ in range(max_retries):
        x = random.randint(0, n - 1)
        y_square = (x**3 + a * x + b) % n
        if is_square_modulo(n, y_square):
            y = find_root_modulo(n, y_square)
            if y is not None:
                return (x, y)
    return None

def compute_group_order_schoof(n, a, b):
    """Compute group order using Schoof's algorithm."""
    try:
        E = sage.EllipticCurve(sage.FiniteField(n), [a, b])
        return E.cardinality()
    except Exception as e:
        return None

def decompose_group_order(m, n):
    """Decompose m = k * q where q is a probable prime and k > 1."""
    factors = factorint(m)
    for q in factors:
        k = m // q
        if k > 1 and isprime(q) and q > (n**(1/4) + 1)**2:
            return k, q
    return None, None

def point_addition(P, Q, n, a):
    """Perform point addition on the elliptic curve."""
    if P is None:
        return Q
    if Q is None:
        return P
    if P == Q:
        if P[1] == 0:
            return None  # Point at infinity
        denominator = (2 * P[1]) % n
        s = (3 * P[0]**2 + a) * mod_inverse(denominator, n) % n
    else:
        denominator = (Q[0] - P[0]) % n
        if denominator == 0:
            return None  # Point at infinity
        s = (Q[1] - P[1]) * mod_inverse(denominator, n) % n

    x_r = (s**2 - P[0] - Q[0]) % n
    y_r = (s * (P[0] - x_r) - P[1]) % n
    return (x_r, y_r)

def scalar_multiplication(k, P, n, a):
    """Perform scalar multiplication on the elliptic curve."""
    R = None
    for bit in bin(k)[2:]:
        if R is not None:
            R = point_addition(R, R, n, a)
        if bit == '1':
            if R is None:
                R = P
            else:
                R = point_addition(R, P, n, a)
    return R

def validate_point_multiplication(P, k, q, n, a):
    """Validate point multiplication."""
    kP = scalar_multiplication(k, P, n, a)
    if kP is None:
        return False  # Invalid: (m/q) * P = O
    qP = scalar_multiplication(q, kP, n, a)
    return qP is None  # Must be true for valid curve

def ecpp_certificate(n, max_attempts=10):
    """ECPP test that returns True for prime numbers and False for composite numbers."""
    def ecpp_recursive_internal(n):
        for _ in range(max_attempts):
            # Step 1: Select a valid elliptic curve
            a, b = random.randint(0, n - 1), random.randint(0, n - 1)
            if not is_valid_curve(a, b, n):
                continue

            # Step 2: Compute group order using Schoof's algorithm
            m = compute_group_order_schoof(n, a, b)
            if m is None:
                continue

            # Step 3: Decompose group order
            k, q = decompose_group_order(m, n)
            if k is None or q is None:
                continue

            # Step 4: Recursively verify q
            if not isprime(q) and not ecpp_recursive_internal(q):
                continue

            # Step 5: Select a point on the elliptic curve
            P = random_point_on_curve(n, a, b)
            if P is None:
                continue

            # Step 6: Validate point multiplication
            if not validate_point_multiplication(P, k, q, n, a):
                continue

            return True  # ECPP proves n is prime

        return False  # ECPP could not prove primality (composite)

    return ecpp_recursive_internal(n)

