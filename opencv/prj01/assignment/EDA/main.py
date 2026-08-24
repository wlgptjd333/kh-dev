# flights (항공기 탑승객 데이터 분석)

# 항공기 탑승객 수에 영향을 준 핵심 요인은 '연도의 흐름(성장)'과 '특정 월(여름 휴가철)'이었습니다.
# 연도 (year): 1949년부터 1960년까지 단 한 해도 빠짐없이 매년 총 탑승객 수가 꾸준히 증가함(상향 추세).
# 성수기 (month): 매년 예외 없이 7월과 8월에 탑승객이 가장 많음 (여름 휴가 시즌의 영향).
# 비수기 (month): 매년 11월은 한 해 중 탑승객이 가장 적은 달로 나타남.
# 상호작용 (연도 x 계절): 연도가 지날수록 전체 탑승객이 늘어날 뿐만 아니라,
# 여름 성수기와 가을/겨울 비수기 간의 '탑승객 수 격차'도 점점 더 크게 벌어지는 특징을 보임.

import seaborn as sns
import matplotlib.pyplot as plt

# 1. 데이터 불러오기
df = sns.load_dataset('flights')
print(df.head())

plt.figure(figsize=(10, 12))

# --- 첫 번째 그래프: 히트맵 (계절성 확인) ---
plt.subplot(2, 1, 1) # 2줄 1칸 중 1번째 자리에 그리기
flights_pivot = df.pivot(index="month", columns="year", values="passengers")
sns.heatmap(flights_pivot, annot=True, fmt="d", cmap="YlGnBu")
plt.title("Number of Passengers (1949-1960) - Heatmap")

# --- 두 번째 그래프: 선 그래프 (연도별 상승 추세 및 성수기/비수기 격차 확인) ---
plt.subplot(2, 1, 2)
sns.lineplot(data=df, x="year", y="passengers", hue="month", marker="o", palette="tab20")
plt.title("Passengers Trend by Month (1949-1960) - Line Plot")
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
plt.grid(True, linestyle='--', alpha=0.6)

# 3. 출력
plt.tight_layout()
plt.show()