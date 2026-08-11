#  열 = [주문ID, 금액, 수량]
import numpy as np

orders = np.array([
    [1, 25000, 2],
    [2, 13000, 1],
    [3, 48000, 3],
    [4,  9000, 1],
    [5, 30000, 1],
])

# 1. 전체 매출(금액 합)
total_revenue = np.sum(orders)
print(total_revenue)
# 2. 평균 주문 금액
mean_revenue = np.mean(orders)
print(mean_revenue)
# 3. 3만원 이상 주문의 주문ID
vip_orders = orders[orders[:,1] >= 30000, 0]
print(vip_orders)
# 4. 가장 비싼 주문의 ID
max_price_index = np.argmax(vip_orders)
print(max_price_index)
# 5. (도전) 단가(금액/수량)가 가장 높은 주문의 ID
# 넘파이는 배열끼리 나누기를 하면 같은 줄에 있는 숫자끼리 알아서 계산해 줍니다!
unit_prices = orders[:, 1] / orders[:, 2]  # [12500, 13000, 16000, 9000, 30000]
max_unit_price_index = np.argmax(unit_prices)
best_unit_id = orders[max_unit_price_index, 0]
print(f"5. 단가가 가장 높은 주문ID: {best_unit_id}")