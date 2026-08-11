import numpy as np

data = np.array([10, np.nan, 30, np.nan, 50])

# 1. 결측치(NaN) 위치 찾기
print("1. 결측치(NaN) 위치 찾기")
is_nan = np.isnan(data)
print(is_nan)
# 2. 결측치 개수
print("\n2. 결측치 개수")
nan_count = np.isnan(data).sum()
print(nan_count)
# 3. NaN 무시하고 평균 (nanmean)
print("3. NaN 무시하고 평균")
nan_mean = np.nanmean(data)
print(nan_mean)
# 4. (도전) NaN을 0으로 채우기
print("NaN 0으로 채우기")
nan_fill = np.where(np.isnan(data), 0, data)
print(nan_fill)