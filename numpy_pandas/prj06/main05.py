import numpy as np

rng = np.random.default_rng(seed=42)

# 1. 주사위(1~6)를 100번 굴린 배열 만들기
result1 = rng.integers(1, 7, (10, 10))
# print(result1)

# 2. 각 눈(1~6)이 몇 번씩 나왔는지 세기
result2 = []
for i in range(1, 7):
    count = np.sum(result1 == i)
    result2.append(count)
print(*result2)

# 3. 나온 값들의 평균
result3 = []
result3.append(np.mean(result1))
print(*result3)

# 4. (도전) 6이 나온 횟수
result4 = np.sum(result1 == 6)
print(result4)
