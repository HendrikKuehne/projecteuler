import numpy as np

max_mult = 1000
multiples_3 = int(max_mult / 3)
multiples_5 = int(max_mult / 5)

mult_sum = sum(set(3 * np.arange(start=1, stop=multiples_3 + 1)).union(5 * np.arange(start=1, stop=multiples_5 + 1)))

print(mult_sum)
print(5 * np.arange(start=1, stop=multiples_5 + 1))