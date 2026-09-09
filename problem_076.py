"""
The basic idea: count the number of ways for every number of positive
integers, and sum them up. Given a number of positive integers that we
want to sum up to 100, the number of different ways to do this is
calculated by the function `IntPartition`.
"""

from functools import cache

@cache
def IntPartition(n: int, k: int) -> int:
    """
    The number of ways to divide `n` elements into `k` sets, where the
    `n` elements are indistinguishable.
    """
    if k == 0: raise ValueError(f"Received k == {k}")
    if n == 0: raise ValueError(f"Received n == {n}")

    if k > n: return 0
    if n == 1: return 1 # Only one element to take from
    if k == 1: return 1 # Only one set to fill
    if n == k: return 1 # As many sets as there are elements

    return IntPartition(n - 1, k - 1) + IntPartition(n - k, k)

targetsum = 100
num_ways = sum([IntPartition(targetsum, k) for k in range(2, targetsum + 1)])

print(f"There are {num_ways} to write {targetsum} as a sum of two or more positive integers.")
