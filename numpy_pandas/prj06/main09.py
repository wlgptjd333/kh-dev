import numpy as np

heat = np.array([[3, 8, 2],
                 [9, 1, 5],
                 [4, 7, 6]])

# 1. 전체 최댓값
result1 = np.max(heat)
print(result1)

# 2. 최댓값의 (행, 열) 위치
result2 = np.unravel_index(np.argmax(heat), heat.shape)
print(result2)

# 3. 각 행의 최댓값
result3 = np.max(heat, axis=1)
print(result3)

# 4. 각 열에서 최댓값이 있는 행 번호
result4 = np.argmax(heat, axis=1)
print(result4)