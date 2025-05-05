from sympy import primerange

# Generate prime numbers up to 1,000,000
primes = list(primerange(2, 1000000))

# Save to CSV file
primes_file_path = "primes.csv"
with open(primes_file_path, "w") as f:
    for prime in primes:
        f.write(str(prime) + "\n")

# Return the file path
primes_file_path


from sympy import isprime

# Generate composite numbers up to 1,000,000
composites = [n for n in range(4, 1000000) if not isprime(n)]

# List of known Carmichael numbers up to 1,000,000
carmichael_numbers = [
    561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341, 41041, 46657, 52633,
    62745, 63973, 75361, 101101, 115921, 126217, 162401, 172081, 188461, 252601, 278545,
    294409, 314821, 334153, 340561, 399001, 410041, 449065, 488881, 512461, 530881,
    552721, 656601, 658801, 670033, 748657, 825265, 879001, 888397, 1082809
]

# Ensure the composite list has 78,498 numbers and contains Carmichael numbers
selected_composites = carmichael_numbers + [n for n in composites if n not in carmichael_numbers][:78498 - len(carmichael_numbers)]

# Save to CSV file
composites_file_path = "composites_with_carmichaels.csv"
with open(composites_file_path, "w") as f:
    for composite in selected_composites:
        f.write(str(composite) + "\n")

# Return the file path
composites_file_path
