import numpy as np

# 데이터 준비
m = np.arange(12)
m = m.reshape(3,4)

# 전치
n = m.T

# 출력
print(m)
print(n)
print(n @ m)