import math
import random
import csv
from gmpy2 import powmod, jacobi
from math import gcd

# Fermat Primality Test
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

# Miller-Rabin Primality Test
def miller_rabin_test(n, k):
    """Return True if n is probably prime, False if composite."""
    if n <= 3:
        return n == 2 or n == 3
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

# Solovay-Strassen Primality Test
def solovay_strassen_test(n, k):
    """Return True if n is probably prime, False if composite."""
    if n <= 3:
        return n == 2 or n == 3
    if n % 2 == 0:
        return False

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

# Read numbers from CSV file
def read_from_lists(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        numbers = []
        for row in reader:
            for num in row:
                if num.isdigit():
                    numbers.append(int(num))
    return numbers


# Compute Accuracy, Precision, Recall, Error Rate, and Confusion Matrix
def compute_accuracy(algorithm, primes, composites, k):
    TP = TN = FP = FN = 0
    false_positives = []

    # Test primes
    for p in primes:
        result = algorithm(p, k)
        if result:  # Predict prime
            TP += 1
        else:       # Predict composite
            FN += 1

    # Test composites
    for c in composites:
        result = algorithm(c, k)
        if not result:  # Predict composite
            TN += 1
        else:           # Predict prime
            FP += 1
            false_positives.append(c)

    # Calculate metrics
    total = TP + TN + FP + FN  # Total numbers tested
    accuracy = (TP + TN) / total if total > 0 else 0
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    error_rate = (FP + FN) / total if total > 0 else 0

    return accuracy, precision, recall, error_rate, TP, FP, TN, FN, false_positives


def main():
    # Paths to CSV files
    primes_file = 'primes.csv'
    composites_file = 'composites_with_carmichaels.csv'

    # Read numbers from the CSV files
    primes = read_from_lists(primes_file)
    composites = read_from_lists(composites_file)

    # Number of iterations for probabilistic tests
    k = 40

    # Test Fermat Primality Test
    fermat_accuracy, fermat_precision, fermat_recall, fermat_error_rate, TP, FP, TN, FN, false_positives = compute_accuracy(
        fermat_primality_test, primes, composites, k
    )
    print("\nFermat Primality Test Results:")
    print(f"Accuracy: {fermat_accuracy:.5f}, Precision: {fermat_precision:.2f}, Recall: {fermat_recall:.2f}, Error Rate: {fermat_error_rate:.2f}")
    print(f"TP: {TP}, FP: {FP}, TN: {TN}, FN: {FN}")
    print("\nFalse Positives (Composites incorrectly identified as primes):")
    print(false_positives)

    # Test Miller-Rabin Primality Test
    mr_accuracy, mr_precision, mr_recall, mr_error_rate, TP, FP, TN, FN, false_positives = compute_accuracy(
        miller_rabin_test, primes, composites, k
    )
    print("\nMiller-Rabin Primality Test Results:")
    print(f"Accuracy: {mr_accuracy:.5f}, Precision: {mr_precision:.2f}, Recall: {mr_recall:.2f}, Error Rate: {mr_error_rate:.2f}")
    print(f"TP: {TP}, FP: {FP}, TN: {TN}, FN: {FN}")
    print("\nFalse Positives (Composites incorrectly identified as primes):")
    print(false_positives)

    # Test Solovay-Strassen Primality Test
    ss_accuracy, ss_precision, ss_recall, ss_error_rate, TP, FP, TN, FN, false_positives = compute_accuracy(
        solovay_strassen_test, primes, composites, k
    )
    print("\nSolovay-Strassen Primality Test Results:")
    print(f"Accuracy: {ss_accuracy:.5f}, Precision: {ss_precision:.2f}, Recall: {ss_recall:.2f}, Error Rate: {ss_error_rate:.2f}")
    print(f"TP: {TP}, FP: {FP}, TN: {TN}, FN: {FN}")
    print("\nFalse Positives (Composites incorrectly identified as primes):")
    print(false_positives)

if __name__ == "__main__":
    main()
