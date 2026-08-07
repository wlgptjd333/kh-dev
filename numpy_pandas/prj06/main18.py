import numpy as np

sales = np.array([10, 20, 30, 40, 50, 60])

# 1. 전체 평균
result1 = np.mean(sales)
print(result1)
# 2. (도전) 3일 이동평균 (연속 3개씩 평균)
result2 = []
for i in range(4):
    window = sales[i:i+3]
    result2.append(np.mean(window))
result2 = np.array(result2)
print(result2)
#    → 결과 길이는 4