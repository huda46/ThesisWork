from sage.all import *

def boneh_durfee_attack(N, e, delta=0.292, m=5, t=30):
    """
    Attempts to recover private exponent d using Boneh-Durfee lattice-based attack.
    :param N: RSA modulus
    :param e: Public exponent
    :param delta: Theoretical limit for d (d < N^delta)
    :param m, t: Parameters for lattice construction
    :return: Private exponent d if found, otherwise None
    """
    PR.<x,y> = PolynomialRing(Zmod(e))
    f = 1 + x * (e*y - 1)   # Approximate equation e * d ≡ 1 (mod φ(N))

    # Construct lattice basis
    X = floor(N ** delta)
    Y = floor(N ** (1 - delta))
    M = []
    
    for i in range(m + 1):
        for j in range(m - i + 1):
            M.append((x^i * y^j * e**(m - i)).coefficients(sparse=False))

    L = Matrix(ZZ, M)
    L = L.LLL()  # Apply lattice reduction

    # Solve for small roots
    for row in L:
        f_ = sum(c * x^i * y^j for ((i, j), c) in row.dict().items())
        roots = f_.small_roots(X=X, Y=Y, beta=delta)
        
        if roots:
            d = int(roots[0])
            return d

    return None

# Example usage
N = 8891257591372151692378239059281516445147094910877073791349276530978630747
e = 179695110007422300542443045469515736987

d = boneh_durfee_attack(N, e)

if d:
    print(f"Recovered private key: {d}")
else:
    print("Attack failed. d might not be small enough or lattice parameters need tuning.")
