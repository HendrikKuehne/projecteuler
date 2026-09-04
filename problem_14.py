import sys
import math

# Transparent cache dictionary
collatz_cache = {1: 1}

def Collatz(n: int) -> int:
    """Implements one step of the Collatz sequence."""
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1

def CollatzLength(M: int) -> int:
    """
    Computes the length of the Collatz chain starting with M 
    by using a custom dictionary cache and the log-base-2 trick.
    """
    # 1. Return from cache if available
    if M in collatz_cache:
        return collatz_cache[M]

    # 2. Check if M is a power of two using bitwise operation
    if (M & (M - 1)) == 0 and M > 0:
        length = int(math.log2(M)) + 1
    else:
    # 3. Calculate normally
        length = 1 + CollatzLength(Collatz(M))

    # 4. Save to cache before returning
    collatz_cache[M] = length
    return length

def main():
    # Wait for command line input from the user
    while True:
        try:
            user_input = input("Enter a positive integer M to find the maximum Collatz chain length for start values <= M: ")
            M = int(user_input)
            if M <= 0:
                print("Alert: Please enter a positive integer > 0.")
                continue
            break
        except ValueError:
            print("Alert: Invalid input. You must type a single integer only. Terminating.")
            sys.exit(1)
        except EOFError:
            print("\nExiting.")
            sys.exit(0)
            
    # Increase recursion limit to avoid RecursionError on deep chains
    sys.setrecursionlimit(max(sys.getrecursionlimit(), 10000))
    
    # Compute all chain lengths from 1 to M
    max_length = 0
    best_start = 1
    
    for i in range(1, M + 1):
        length = CollatzLength(i)
        if length > max_length:
            max_length = length
            best_start = i
            
    print(f"The maximum Collatz chain length for starting numbers <= {M} is {max_length} (starting at {best_start}).")
    
    # Optional: You could inspect the cache now, e.g.:
    # print(f"Cache size: {len(collatz_cache)}")
    # print(f"Length of 13: {collatz_cache.get(13)}")

if __name__ == "__main__":
    main()
