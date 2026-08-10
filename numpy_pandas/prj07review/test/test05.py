# shape 변환
import numpy as np

x = np.linspace(1, 24, 24)
x = x.astype(int)
x = x.reshape(2, 3, 4)

print(x.shape)
print(x.ndim)
print(x.size)
print(x.dtype)
print(x)
