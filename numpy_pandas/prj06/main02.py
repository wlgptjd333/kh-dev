import numpy as np

stores = np.array(["강남", "홍대", "잠실"])
# 4일 × 3지점 매출(만원)
sales = np.array([[120, 90, 100],
                  [130, 95, 110],
                  [100, 80,  90],
                  [140, 100, 120]])

# 1. 지점별 총매출 (열별 합계)
result1 = np.sum(sales, axis = 0)
print(result1)
# 2. 일별 총매출 (행별 합계)
result2 = np.sum(sales, axis = 1)
print(result2)
# 3. 전체 평균 매출
result3 = np.average(sales)
print(result3)
# 4. 매출이 가장 높은 지점 이름
result4 = stores[np.argmax(np.sum(sales,axis = 0))]
print(result4)