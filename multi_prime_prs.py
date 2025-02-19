import math
import random

SAFE_PRIME_LIMITS = {1024: 3, 2048: 3, 4096: 4, 8192: 5}

def bit_length(n):
    """Compute the bit-length of a number N."""
    return n.bit_length()

def estimate_prime_size(N, r):
    """Estimate the size of each prime factor if N is an r-prime RSA modulus."""
    bits_N = bit_length(N)
    return bits_N // r  # Approximate size of each prime

def pollards_rho(N):
    """Finds a non-trivial factor of N using Pollard's Rho."""
    if N % 2 == 0:
        return 2
    x = random.randint(2, N - 1)
    y = x
    c = random.randint(1, N - 1)
    d = 1

    def f(x, N, c):
        return (x * x + c) % N

    while d == 1:
        x = f(x, N, c)
        y = f(f(y, N, c), N, c)
        d = math.gcd(abs(x - y), N)

    return d if d != N else None

def ecm_simulation(N, prime_bits):
    """Simulated ECM method to find a factor of N."""
    B = 2**prime_bits  # Upper bound for prime search
    for p in range(2, B):
        if N % p == 0:
            return p  # Return first small factor found
    return None

def determine_factoring_method(N, r):
    """Determine if ECM or GNFS should be used based on safe prime limits."""
    modulus_bits = bit_length(N)
    r_max = SAFE_PRIME_LIMITS.get(modulus_bits, None)

    if r_max is None:
        print("Unsupported modulus size!")
        return None

    if r > r_max:
        prime_bits = estimate_prime_size(N, r)
        print(f"Using ECM: estimated prime size is {prime_bits} bits.")
        return "ECM", prime_bits
    else:
        print("Using GNFS.")
        return "GNFS", None

def factor_N_completely(N, r):
    """Fully factor N into all prime components."""
    factors = []
    method, prime_bits = determine_factoring_method(N, r)

    while N > 1:
        if method == "ECM":
            factor = ecm_simulation(N, prime_bits)
            if factor:
                print(f"Found factor using ECM: {factor}")
                factors.append(factor)
                N //= factor
                continue  # Continue factoring the new smaller N
        elif method == "GNFS":
            factor = pollards_rho(N)
            if factor:
                print(f"Found factor using Pollard’s Rho: {factor}")
                factors.append(factor)
                N //= factor
                continue  # Continue factoring the new smaller N
        else:
            print("Factoring failed: GNFS required for further attempts.")
            break

    return factors

# Example 4-prime RSA modulus (for testing)
N = 113332090023462300679849704488734092545177458348009818380962235081786371756930138282268756018893172240323434046786858845802802651551047691281687345319806961336276944052245323199594091910534816244830965714099756271937025204248634945207477502870610189621191319450134671259233760978683947908584453185220999062323  
r = 4  # Assume N is a 4-prime RSA modulus

# Run the attack to find all prime factors
print("Factoring RSA Modulus...")
print("Bit-length of N:", bit_length(N))

factors = factor_N_completely(N, r)
print("All Prime Factors:", factors)
