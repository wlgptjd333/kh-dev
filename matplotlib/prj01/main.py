# import 및 글자 깨짐 처리
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = "Malgun Gothic"
plt.rcParams['axes.unicode_minus'] = False

# 데이터 준비 (x, y 좌표 세트)
month = ["1월", "2월", "3월", "4월", "5월", "6월"]
gangnam = [120, 135, 128, 150, 175, 210]  # 강남점
hongdae = [95, 110, 130, 125, 160, 185]  # 홍대점

# arr = np.linspace(1, 6, 6)
fig, ax = plt.subplots()

# 도화지, 차트 준비
# 강남점
ax.plot(month, gangnam, marker="o", label="강남점", color="blue", markersize=5, alpha=0.5, linewidth=3)
# 홍대점
ax.plot(month, hongdae, marker="^", label="홍대점", color="red", markersize=5, alpha=0.5, linewidth=3)
# 월별 평균선
monthly_mean = [(gangnam + hongdae) / 2 for gangnam, hongdae in zip(gangnam, hongdae)]
ax.plot(month, monthly_mean, label = "월별 평균", color="green", linestyle="--", linewidth=1.5)

# 차트 꾸미기
# ax.set_title("강남/홍대 지점별 월매출")
ax.set_xlabel("월 (Month)", fontsize=15)
ax.set_ylabel("매출 (단위: 만원)", fontsize=15)
ax.set_ylim(0, 230)
ax.grid(alpha=0.3)

# 최고 매출
max_sales = max(gangnam)
max_month = "6월"
ax.annotate(f"최고 매출 {max_sales}만원", xy=(max_month, max_sales), xytext=("4월", 190),
            arrowprops=dict(arrowstyle="->", color="red"), fontsize=10)

# 평균 구하기
total_mean = (sum(gangnam) + sum(hongdae)) / (len(gangnam) + len(hongdae))
ax.set_title(f"상반기 월별 매출 추이 (전체 평균 {total_mean:.1f}만원)")
# ax.axhline(y=total_mean, color="black", linestyle="--", label="전체평균선")


# 차트 그리기
ax.legend()
plt.savefig("result.png")
plt.show()
