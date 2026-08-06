import numpy as np

data = np.array([15, 8, 23, 42, 4, 16, 30])
grid = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

print(data[2:5])

print(data[data > 20])

print(grid[:,1])