import numpy as np

data = np.array([10, 20, 30, 40, 50, 60])
idx  = np.array([0, 2, 4])

# 1. idx 위치의 값들만 뽑기
result1 = np.array(data[idx])
print(result1)

# 2. 0,3,5번째 값을 한 번에 뽑기
num = [0,3,5]
result2 = np.array(data[num])
print(result2)

# 3. 결과가 [50, 10, 30]이 되도록 인덱스로 재배열
num2 = [4,0,2]
result3 = np.array(data[num2])
print(result3)

# 4. (도전) 짝수 인덱스(0,2,4...)의 값만
result4 = np.array(data[idx%2==0])
print(result4)