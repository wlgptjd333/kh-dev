# 입출금 내역 (양수=입금, 음수=출금)
import numpy as np

trans = np.array([100, -30, 50, -80, 200, -60])

# 1. 거래별 누적 잔액 (시작 잔액 0)
cum_gold = np.cumsum(trans)
print(cum_gold)

# 2. 최종 잔액
total_gold = 0
total_gold += np.sum(trans)
print(total_gold)

# 3. 잔액이 가장 많았던 시점의 잔액
max_gold = np.max(cum_gold)
print(max_gold)

# 4. (도전) 잔액이 마이너스가 된 적이 있는가?
minus_gold = (cum_gold < 0).any()
print(minus_gold)