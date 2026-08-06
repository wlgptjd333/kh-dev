# axis
import numpy as np

x = np.arange(1, 13)
x = x.reshape((3, -1))


# 연산
result = np.sum(x, axis=0)
print(x)
print("=====")
print(result)
