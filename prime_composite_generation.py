import sympy

# Generate primes up to a limit
def generate_primes(limit):
    return list(sympy.primerange(2, limit))

# Save to CSV
def save_to_csv(numbers, filename):
    import csv
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([[num] for num in numbers])

primes = generate_primes(1_000_000_000)
save_to_csv(primes, 'primes10b.csv')

def generate_composites(primes, limit):
    composites = set(range(4, limit))
    composites -= set(primes)  # Remove primes from the list
    return sorted(composites)

primes = generate_primes(1_000_000_000)
composites = generate_composites(primes, 1_000_000_000)
save_to_csv(composites, 'composites1b.csv')
