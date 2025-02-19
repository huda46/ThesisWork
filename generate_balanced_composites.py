import random
import csv

# Carmichael numbers
carmichael_numbers = [
    561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841, 29341,
    41041, 46657, 52633, 62745, 63973, 75361, 101101, 115921
]

# Sampling distribution and target samples
ranges = [
    (1, 10000, 3140),
    (10001, 100000, 7850),
    (100001, 200000, 8634),
    (200001, 300000, 9478),
    (300001, 400000, 9478),
    (400001, 500000, 8634),
    (500001, 1000000, 31284)
]

def read_composites(file_path):
    """Read composites from a CSV file."""
    composites = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            composites.append(int(row[0]))
    return composites

def sample_composites_with_carmichael(composites, carmichaels, ranges, total_samples):
    """Sample composites proportionally, ensuring Carmichael numbers are included."""
    sampled_composites = []
    remaining_carmichaels = set(carmichaels)

    for start, end, num_samples in ranges:
        # Filter composites within the current range
        range_composites = [x for x in composites if start <= x <= end]
        # Ensure Carmichael numbers within this range are included
        range_carmichaels = [x for x in remaining_carmichaels if start <= x <= end]
        remaining_carmichaels -= set(range_carmichaels)

        # Calculate how many more composites are needed after adding Carmichael numbers
        additional_samples = num_samples - len(range_carmichaels)
        if additional_samples < 0:
            raise ValueError("Too many Carmichael numbers in range!")

        # Sample remaining composites proportionally
        sampled = random.sample(range_composites, additional_samples)
        sampled_composites.extend(range_carmichaels + sampled)

    # Ensure total matches the target
    if len(sampled_composites) != total_samples:
        raise ValueError("Sampling error: total samples do not match target.")
    return sampled_composites

def save_composites_to_csv(file_path, composites):
    """Save the list of composites to a CSV file."""
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows([[x] for x in composites])

def main():
    # File paths
    input_file = "composites.csv"  # Path to the input composites file
    output_file = "balanced_composites_with_carmichaels.csv"  # Path to the output file

    # Read composites from the CSV
    composites = read_composites(input_file)

    # Target number of samples
    num_samples = 78498

    # Generate the balanced sample
    balanced_composites = sample_composites_with_carmichael(composites, carmichael_numbers, ranges, num_samples)

    # Save to CSV
    save_composites_to_csv(output_file, balanced_composites)

    print(f"Balanced composite list saved to {output_file}")
    print(f"Total composites: {len(balanced_composites)} (includes {len(carmichael_numbers)} Carmichael numbers)")

# Run the program
main()
