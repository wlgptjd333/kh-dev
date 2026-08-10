# 배열 생성 및 속성

import numpy as np

shape = (100,100)
v = 123
result = np.zeros(shape)
result = np.ones(shape)
result = np.full((shape), v)
result = np.eye(2)

print(result.shape)
print(result.ndim)
print(result)