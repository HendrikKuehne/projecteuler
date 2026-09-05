from functools import cache

@cache
def is_prime(n: int) -> bool:
    for k in range(2, n):
        if n % k == 0: return False
    return True

@cache
def get_prime_factors(n: int) -> tuple[int]:
    """
    Get all prime factors of `n`. If `n` is prime itself,
    returns `(n,)`.
    """
    if is_prime(n): return (n,)

    k = 2
    while n % k != 0 and k < n: k += 1
    if k == n: raise RuntimeError("This code should be dead; does the function is_prime work properly?")

    f1 = k
    f2 = int(n / k)

    return get_prime_factors(f1) + get_prime_factors(f2)

factors = get_prime_factors(600851475143)
print(sorted(factors))
