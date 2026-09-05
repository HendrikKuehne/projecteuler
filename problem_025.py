"""
The general idea: To find out if a new digit is required, it suffices
to look at the first digits of the previous two numbers. If their
sum is larger than or equal to ten, a new digit is required.
"""
import math

class FibNum:
    """
    I am saving Fibonacci numbers as floating-point numbers
    with mantissa and exponent.
    """
    resolution: int = None
    m: float = None
    """Mantissa."""
    e: int = None
    """Exponent."""

    def truncate_decimals(self, number: float):
        """Truncate decimal respresentation of a number."""
        factor = 10 ** self.resolution
        # Add a small epsilon to prevent floating point inaccuracies from truncating down
        return int(number * factor + 1e-9) / factor

    def __init__(self, m: float, e: int, resolution: int = 3) -> None:
        if m < 0: raise ValueError("Mantissa must be larger than or equal to zero.")
        if e < 0: raise ValueError("Exponent must be larger than zero.")

        self.resolution = resolution
        """Maximum number of digits of the mantissa that are retained."""

        if m == 0:
            self.m: float = 0
            self.e: int = 0
            return

        elif math.log10(m) > 0:
            # mantissa is one or above
            self.m: float = m * 10 ** (-int(math.log10(m)) - 1)
            self.e: int = int(math.log10(m)) + 1 + e

        else:
            # Mantissa is between 0 and 1, and can be used as-is
            self.m: float = m
            self.e: int = e

        # Truncate decimals of the mantissa
        self.m = self.truncate_decimals(self.m)

        return

    def __add__(self, rhs: "FibNum") -> "FibNum":
        """
        Addition proceeds as follows:
        + Pad both numbers to the same exponent.
        + Add as usual.
        """
        if self.e == rhs.e:
            m_sum = self.m + rhs.m
            return FibNum(m_sum, self.e, self.resolution)

        if self.e < rhs.e:
            m_sum = self.m * 10 ** (self.e - rhs.e) + rhs.m
            return FibNum(m_sum, rhs.e, self.resolution)

        if self.e > rhs.e:
            m_sum = self.m + rhs.m * 10 ** (rhs.e - self.e)
            return FibNum(m_sum, self.e, self.resolution)

    def __repr__(self): return str(self.m * 10 ** self.e)


if __name__ == "__main__":
    resolution = 7
    """I found that resolution = 5 is the first resolution that is accurate enough."""
    F_sequence = [FibNum(1, 0, resolution), FibNum(1, 0, resolution)]

    while F_sequence[-1].e < 1000:
        F_sequence.append(F_sequence[-2] + F_sequence[-1])

    print(len(F_sequence))
