import secrets
import math
import random
def generate_1024_bit_number():
    # Generate a 1024-bit random number
    number = secrets.randbits(1024)
    return number

def bit_length(n):
    """Compute the bit-length of a number N."""
    return n.bit_length()

# Example usage
if __name__ == "__main__":
    num = generate_1024_bit_number()
    print("Bit-length of num:", bit_length(num))
    print("Generated 1024-bit number:", num)