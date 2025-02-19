from Trial_division import compare_algorithms
from sympy import sympify
from math import gcd

def main():
    while True:
        try:
            print("\n=== Prime Number Testing ===")
            print("Choose an option for the type of number you want to test:")
            print("1. Custom mathematical expression (e.g., 10**5 + 34225 or 2^10 + 1)")
            print("2. Mersenne number (2^n - 1)")
            print("3. General number of the form 2^n + 1")
            print("4. Standard integer input (e.g., 986578697)")
            print("5. Exit")
            choice = input("Enter your choice (1, 2, 3, 4, or 5): ")

            if choice == '5':
                print("Exiting the program. Goodbye!")
                break

            if choice == '1':
                expression = input("Enter a number to test (e.g., 10**5 + 34225 or 2^10 + 1): ")
                expression = expression.replace('^', '**')
                try:
                    expression = sympify(expression)
                    n = int(expression)
                except Exception as e:
                    print(f"Invalid mathematical expression: {e}")
                    continue

            elif choice == '2':
                exp = int(input("Enter the exponent n for the Mersenne number (2^n - 1): "))
                if exp <= 0:
                    print("Exponent n must be a positive integer.")
                    continue
                try:
                    n = (2 ** exp) - 1
                    print(f"Testing the Mersenne number: 2^{exp} - 1")
                except OverflowError:
                    print("The exponent is too large. Choose a smaller exponent.")
                    continue

            elif choice == '3':
                exp = int(input("Enter the exponent n for the number (2^n + 1): "))
                if exp <= 0:
                    print("Exponent n must be a positive integer.")
                    continue
                try:
                    n = (2 ** exp) + 1
                    print(f"Testing the number: 2^{exp} + 1")
                except OverflowError:
                    print("The exponent is too large. Choose a smaller exponent.")
                    continue

            elif choice == '4':
                n = int(input("Enter the standard integer you want to test: "))
                if n <= 0:
                    print("The number must be a positive integer.")
                    continue
                print(f"Testing the number: {n}")

            else:
                print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
                continue

            k = int(input("Enter the number of iterations for probabilistic tests (default: 10): ") or "10")

            # Compare all algorithms, including ECPP
            try:
                compare_algorithms(n, k, 1, 1, 22, 11)  # ECPP is now included in this call
            except Exception as e:
                print(f"Error during algorithm comparison: {e}")

        except ValueError:
            print("Invalid input. Please enter valid integers or expressions.")
        except SyntaxError:
            print("Invalid syntax. Please enter a valid mathematical expression.")
        except OverflowError:
            print("The number is too large to handle. Try a smaller number.")

        print("\nWould you like to test another number? (yes/no)")
        retry = input().lower()
        if retry not in ['yes', 'y']:
            print("Exiting the program. Goodbye!")
            break

if __name__ == "__main__":
    main()
