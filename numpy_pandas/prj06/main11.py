import numpy as np

# 1. 0~11 정수 배열을 만들어 3×4 행렬로
result1 = np.arange(12).reshape(3, 4)
print(result1)

# 2. 그 행렬의 shape과 차원 수(ndim)
result2 = [np.shape(result1), np.ndim(result1)]
print(result2)

# 3. 0부터 1까지 균등하게 5개 나누기
result3 = np.linspace(0, 1, 5)
print(result3)

# 4. (도전) 위 3×4 행렬을 다시 1차원으로
result4 = result1.reshape(-1)
print(result4)