# N차원 배열
import numpy as np

matrix = [
    [1,2,3],
    [4,5,6],
]

np.array(matrix)

result = np.array([matrix,matrix,matrix,matrix])

print(result.shape)
print(result.ndim)
print(result)