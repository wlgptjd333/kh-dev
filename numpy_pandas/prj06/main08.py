import numpy as np

data = np.array([10, 20, 30, 40, 50])

# 1. min-max 정규화 → 0~1 범위로
min_x = np.min(data)
max_y = np.max(data)
result1 = (data - min_x) / (max_y - min_x)
print(result1)

# 2. z-score 표준화 → 평균0, 표준편차1
mean_x = np.mean(data)
std_x = np.std(data)
result2 = (data - mean_x) / std_x
print(result2)

# 3. (도전) 아래 2D를 '열별'로 min-max 정규화
features = np.array([[1, 100],
                     [2, 200],
                     [3, 300]])

min_cols = np.min(features, axis=0)
max_cols = np.max(features, axis=0)

result3 = (features - min_cols) / (max_cols - min_cols)
print(result3)