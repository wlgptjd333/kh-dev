# review
import numpy as np

# data
a = np.arange(6)
m = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [3, 7, 1]
])

# ???
a = a.reshape(2, 3)
result = np.min(m, axis=0)

# print
print(a)
print(m)
print(result)
