import numpy as np

a = np.array([3, 4])
b = np.array([1, 2])

# 1. a와 b의 내적 (dot)
result1 = np.dot(a, b)
print(result1)

# 2. a의 크기(길이, norm)
result2 = np.linalg.norm(a)
print(result2)
# 3. a와 b 사이의 유클리드 거리
result3 = np.linalg.norm(a - b)
print(result3)
# 4. (도전) a 방향의 단위벡터
result4 = a/result2
print(result4)