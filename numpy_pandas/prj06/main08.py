data = np.array([10, 20, 30, 40, 50])

# 1. min-max 정규화 → 0~1 범위로
# 2. z-score 표준화 → 평균0, 표준편차1
# 3. (도전) 아래 2D를 '열별'로 min-max 정규화
features = np.array([[1, 100],
                     [2, 200],
                     [3, 300]])