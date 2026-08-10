import numpy as np

# 간격
result = np.arange(1,10,3)
print(result)

#개수
result = np.linspace(0,1,5)
result = result.astype(int)
print(result.shape)
print(result.ndim)
print(result.size)
print(result.dtype)
print(result)
