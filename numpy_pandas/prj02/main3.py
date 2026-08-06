import numpy as np

x = np.array([
    [1, 2.2, 3],
    [4, 5, 6],
    [7, 8, 9],
], dtype="float")

print(x)
print("x.shape : ", x.shape)
print("x.ndim : ", x.ndim)
print("x.size : ", x.size)
print("x.dtype : ", x.dtype)

result = x.astype("int")
print(result)