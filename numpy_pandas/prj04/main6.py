import numpy as np

a = np.arange(12)
m = np.array([
    [1, 2, 3],
    [4, 5, 6],
])
row = np.array([10,20,30])

# 브로드캐스팅
# result = a * 2
result = m @ row

print(result)
