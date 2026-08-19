# 총 식사 금액 : total_bill
# 팁 금액 : tip
# 일행 인원수 : size
# 성별 : sex
# 흡연 여부 : smoker
# 요일 : day
# 시간대 : time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("data/tips.csv", encoding="utf-8-sig")

# 한글 폰트 설정
plt.rcParams["font.family"] = ["Malgun Gothic"]
plt.rcParams["axes.unicode_minus"] = False

fig, ax = plt.subplots(2, 2, figsize=(10, 8))


# =========================================================
# 0. 데이터 파악
# =========================================================

print(df.head())
print(df.shape)
df.info()


# =========================================================
# 1. total_bill 히스토그램
# =========================================================

ax[0, 0].hist(
    df["total_bill"],
    bins=20
)

ax[0, 0].set_title("총 식사 금액 분포")
ax[0, 0].set_xlabel("총 식사 금액")
ax[0, 0].set_ylabel("빈도")


# =========================================================
# 2. 요일별 total_bill 박스플롯
# =========================================================

days = ["Thur", "Fri", "Sat", "Sun"]

data = [
    df.loc[df["day"] == day, "total_bill"]
    for day in days
]

ax[0, 1].boxplot(
    data,
    tick_labels=days
)

ax[0, 1].set_title("요일별 총 식사 금액")
ax[0, 1].set_xlabel("요일")
ax[0, 1].set_ylabel("총 식사 금액")


# =========================================================
# 3. total_bill과 tip 산점도
# =========================================================

ax[1, 0].scatter(
    df["total_bill"],
    df["tip"]
)

ax[1, 0].set_title("총 식사 금액과 팁의 관계")
ax[1, 0].set_xlabel("총 식사 금액")
ax[1, 0].set_ylabel("팁")


# =========================================================
# 4. 요일별 주문 건수 막대그래프
# =========================================================

day_count = df["day"].value_counts()

# 원하는 요일 순서
day_count = day_count.reindex(days)

ax[1, 1].bar(
    day_count.index,
    day_count.values
)

ax[1, 1].set_title("요일별 주문 건수")
ax[1, 1].set_xlabel("요일")
ax[1, 1].set_ylabel("주문 건수")


# 그래프 간격 자동 조정
plt.tight_layout()

plt.show()