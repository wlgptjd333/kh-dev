import numpy as np

x = np.array([[10, 20, 30, 40, 50]])

result = np.sum(x)
result += np.mean(x)
result += np.std(x)
result += np.min(x)
result += np.max(x)
result += np.median(x)

'''
합계
평균
표준편차
최소값
최대값
중앙값
where
'''

rng = np.random.default_rng()

result = rng.normal(90,10, size=10)
print(result)
