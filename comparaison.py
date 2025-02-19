import math
import random
import time
from tabulate import tabulate
import matplotlib.pyplot as plt

# Trial division algorithm
def trial_division(n):
    """Return True if n is prime, False if composite."""
    if n < 2:
        return False
    if n in [2, 3]:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    a = math.floor(math.sqrt(n))
    for i in range(5, a + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

# Fermat primality test
def fermat_primality_test(n, k):
    """Return True if n is probably prime, False if composite."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False
    return True

# Miller-Rabin primality test
def miller_rabin_test(n, k):
    """Return True if n is probably prime, False if composite."""
    if n < 2:
        return False
    if n in [2, 3]:
        return True
    if n % 2 == 0:
        return False
    
    s = 0
    t = n - 1
    while t % 2 == 0:
        t //= 2
        s += 1

    for _ in range(k):
        a = random.randint(2, n - 2)
        b = pow(a, t, n)
        if b == 1 or b == n - 1:
            continue
        for _ in range(s - 1):
            b = pow(b, 2, n)
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
        jacobi = 1
        temp_a = a
        temp_n = n
        while temp_a != 0:
            while temp_a % 2 == 0:
                temp_a //= 2
                if temp_n % 8 in [3, 5]:
                    jacobi = -jacobi
            
            temp_a, temp_n = temp_n, temp_a
            if temp_a % 4 == 3 and temp_n % 4 == 3:
                jacobi = -jacobi
            temp_a %= temp_n

        if temp_n == 1:
            jacobi *= 1
        else:
            jacobi = 0

        # Modular exponentiation and comparison
        mod_exp = pow(a, (n - 1) // 2, n)
        if mod_exp != (jacobi % n):
            return False
    return True

def compare_algorithms(n, k):
    """Compare the execution time and results of various primality tests."""
    print("Calculations may take some time. Please wait...\n")
    
    results = []

    # Timing Trial Division
    print("Running Trial Division...")
    start_time = time.perf_counter()
    trial_result = trial_division(n)
    trial_time = time.perf_counter() - start_time
    results.append(["Trial Division", trial_result, trial_time])
    print("Trial Division completed.\n")
    
    # Timing Fermat Primality Test
    print("Running Fermat Primality Test...")
    start_time = time.perf_counter()
    fermat_result = fermat_primality_test(n, k)
    fermat_time = time.perf_counter() - start_time
    results.append(["Fermat Test", fermat_result, fermat_time])
    print("Fermat Primality Test completed.\n")
    
    # Timing Miller-Rabin Primality Test
    print("Running Miller-Rabin Primality Test...")
    start_time = time.perf_counter()
    miller_rabin_result = miller_rabin_test(n, k)
    miller_rabin_time = time.perf_counter() - start_time
    results.append(["Miller-Rabin Test", miller_rabin_result, miller_rabin_time])
    print("Miller-Rabin Primality Test completed.\n")
    
    # Timing Solovay-Strassen Test
    print("Running Solovay-Strassen Test...")
    start_time = time.perf_counter()
    solovay_strassen_result = solovay_strassen_test(n, k)
    solovay_strassen_time = time.perf_counter() - start_time
    results.append(["Solovay-Strassen Test", solovay_strassen_result, solovay_strassen_time])
    print("Solovay-Strassen Test completed.\n")
    
    # Display results as a table
    print(tabulate(results, headers=["Algorithm", "Result", "Time (s)"], tablefmt="grid"))

    # Plot results
    algorithms = [row[0] for row in results]
    times = [row[2] for row in results]
    plt.bar(algorithms, times)
    plt.ylabel("Runtime (seconds)")
    plt.title(f"Primality Testing Performance for n = {n}")
    plt.show()

def main():
    try:
        print("Welcome to the Primality Testing Program!")
        print("1: Test a custom number")
        print("2: Test a Mersenne number (2^n - 1)")
        print("3: Test a number in the form (2^n + 1)")
        
        choice = input("Enter your choice (1, 2, or 3): ")
        
        if choice == '1':
            expression = input("Enter a number to test if it is prime (e.g., 10**5 + 34225): ")
            m = eval(expression)
        elif choice == '2':
            n = int(input("Enter the exponent n for the Mersenne number (2^n - 1): "))
            m = (2 ** n) - 1
        elif choice == '3':
            n = int(input("Enter the exponent n for the number (2^n + 1): "))
            m = (2 ** n) + 1
        else:
            print("Invalid choice.")
            return

        k = int(input("Enter the number of iterations for the probabilistic tests: "))
        compare_algorithms(m, k)

    except ValueError:
        print("Invalid input. Please enter valid integers or expressions.")
    except SyntaxError:
        print("Invalid syntax. Please enter a valid mathematical expression.")
    except OverflowError:
        print("The number is too large to handle. Try a smaller number.")

if __name__ == "__main__":
    main()
