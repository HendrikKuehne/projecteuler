from functools import cache

@cache
def LaggedFibonacci(k: int) -> int:
    """
    A [lagged Fibonacci generator](https://en.wikipedia.org/wiki/Lagged_Fibonacci_generator)
    can be periodic! The period of this one should be on the order of
    1000000, however; let's pray this doesn't become a problem.
    """
    if k < 1 or int(k) != k:
        raise ValueError(f"k must be a positive integer; received {k}")

    if k < 56: return (100003 - 200003 * k + 300007 * k ** 3) % 1000000
    else: return (LaggedFibonacci(k - 24) + LaggedFibonacci(k - 55)) % 1000000


class DisjointSetUnion:
    """
    Keeping track of the connectedness of elements through
    as-shallow-as-possible trees.
    """

    def __init__(self, n: int):
        """
        Creates a data structure with `n` nodes. Initially, all
        nodes are disconnected, i.e., all trees are composed of
        one node only.
        """
        # parent[i] == i means i is its own root; so initially,
        # all nodes are their own roots and thus all trees have
        # size one.
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, i: int) -> int:
        """
        Find and return the root of node `i`.
        """
        path = []
        while self.parent[i] != i:
            path.append(i)
            i = self.parent[i]

        # Path compression to make future lookups more efficient:
        # point all visited nodes directly to the root.
        for node in path:
            self.parent[node] = i

        return i

    def union(self, i: int, j: int) -> bool:
        """
        Declare that nodes `i` and `j` are connected.
        Returns `True` if nodes have not been connected
        previously and are now merged; returns `False`
        otherwise.
        """
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i == root_j:
            return False  # Already in the same component

        # Union by size: attach smaller component under
        # larger component. This is done in order to keep
        # the trees as shallow as possible.
        if self.size[root_i] < self.size[root_j]:
            root_i, root_j = root_j, root_i

        self.parent[root_j] = root_i
        self.size[root_i] += self.size[root_j]

        return True

    def component_size(self, i: int) -> int:
        """
        Size of component attached to node `i`.
        """
        return self.size[self.find(i)]


if __name__ == "__main__":
    pm_number = 524287
    n_users = 1000000
    target_frac = .99

    friends = DisjointSetUnion(n_users)

    call_idx = 1
    call_successes = 0
    while friends.component_size(pm_number) < target_frac * n_users:
        caller1 = LaggedFibonacci(2 * call_idx - 1)
        caller2 = LaggedFibonacci(2 * call_idx)
        call_idx += 1

        if caller1 == caller2: continue
        else: call_successes += 1

        friends.union(caller1, caller2)

    print(f"After {call_successes} successful calls, {target_frac * n_users} people are friends with the prime minister.")
