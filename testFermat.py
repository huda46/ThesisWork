import math
import random
import time
from gmpy2 import powmod, jacobi
from math import gcd, log, isqrt
from random import randint
from sympy import mod_inverse, isprime, symbols, expand, Mod

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

def main():
    try:
        print("Welcome to the Fermat Primality Test!")
        while True:
            user_input = input("\nEnter a number to test for primality (or 'q' to quit): ")
            if user_input.lower() == 'q':
                print("Exiting the Fermat Primality Test. Goodbye!")
                break

            n = int(user_input)
            if n <= 1:
                print("Please enter a number greater than 1.")
                continue

            # Number of iterations for the test
            k = int(input("Enter the number of iterations for the test (e.g., 5): "))

            # Perform the Fermat test
            start_time = time.perf_counter()
            result = fermat_primality_test(n, k)
            elapsed_time = time.perf_counter() - start_time

            # Output result
            if result:
                print(f"The number {n} is probably prime.")
            else:
                print(f"The number {n} is composite.")
            print(f"Time taken for the test: {elapsed_time:.9f} seconds")

    except ValueError:
        print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    main()
