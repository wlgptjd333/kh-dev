# Bool 인덱싱
import numpy as np

m = np.linspace(1, 5, 5).astype(int)
mask = m > 3

print(m.shape)
print(m.ndim)
print(m.size)
print(m.dtype)
print(m[mask])
print(m[(m > 3) & (m < 5)])
