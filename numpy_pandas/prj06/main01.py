# 일주일 기온 통계

import numpy as np

temps = np.array([12, 15, 18, 14, 20, 22, 17])  # 월~일 기온(℃)

# 1. 평균 기온
avg_temp = np.mean(temps)
print(avg_temp)

# 2. 가장 더운 날과 추운 날의 기온
min_temp = np.min(temps)
print(min_temp)
max_temp = np.max(temps)
print(max_temp)

# 3. 기온의 표준편차
std_temp = np.std(temps)
print(std_temp)

# 4. 중앙값
mid_temp = np.median(temps)
print(mid_temp)

# 5. 평균보다 더운 날은 몇번 있었나?
how_many_higher_avg_temp = np.sum(temps > mid_temp)
print(how_many_higher_avg_temp)