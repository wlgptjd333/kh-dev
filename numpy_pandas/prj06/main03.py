import numpy as np

players = np.array(["A", "B", "C", "D", "E"])
score   = np.array([320, 150, 480, 275, 390])

# 1. 점수를 오름차순 정렬
result1 = np.sort(score)
print(result1)

# 2. 높은 점수 순으로 플레이어 이름 나열
result2 = players[np.argsort(score)[::-1]]
print(result2)

# 3. 상위 3명
result3 = players[np.argsort(score)[::-1][:3]]
print(result3)

# 4. 1등과 꼴찌 이름
result4 = players[np.argsort(score)[::-1][:1]]
result4_2 = players[np.argsort(score)[::][:1]]
print(result4)
print(result4_2)