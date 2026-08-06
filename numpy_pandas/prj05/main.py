import numpy as np

# data
a = [
    [1, 2],
    [3, 4],
]
b = [
    [5, 6],
    [7, 8],
]
a = np.array(a)
b = np.array(b)
x = np.array([100, 50, 80, 30])

# 통계 함수
# result = np.sum(x)
# result = np.max(x)
# resutl = np.min(x)
# result = np.mean(x)
# result = np.median(x)
# result = np.std(x)

# 집계 , axis 0 1

# 정렬
# result = np.sort(x)
# result = np.argsort(x)
# result = np.argmax(x)

# where
# result = np.where(x > 60, "합격", "불합격")

# random
g = np.random.default_rng(42)
# result = g.random(3)
# 결과 출력
# result = g.integers(1,7,size=3)
result = g.normal(0, 10, size=3)

# 행렬 곱
# result = a @ b

# inv
result = np.linalg.inv(a)

# 파일
np.save("data.npy", x)
result = np.load("data.npy")

# 결과 출력
print(result)
