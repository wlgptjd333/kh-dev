import csv

# 날짜,도시,최고기온,최저기온,강수량

with open("weather.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    data = list(reader)

if data:
    print(data[0])
else:
    print("데이터가 없습니다.")

# 전체 관측
total = len(data)
print(f"[전체 관측] {total}건")

# 비 온 날
rain_day = 0

for row in data:
    rain = float(row["강수량"])

    if rain > 0:
        rain_day += 1

print(f"비 온 날: {rain_day}건 ({round((rain_day/total)*100, 1)}%)")

# 도시별 평균 최고기온
sum_temp = {}
count_temp = {}

for row in data:
    city = row["도시"]
    temp = float(row["최고기온"])

    # 최고기온 합계
    sum_temp[city] = sum_temp.get(city, 0) + temp

    # 도시별 개수
    count_temp[city] = count_temp.get(city, 0) + 1

# 평균 계산
avg_highest_temp = {}

for city in sum_temp:
    avg_highest_temp[city] = sum_temp[city] / count_temp[city]

for city, avg in avg_highest_temp.items():
    print(f"{city}: {avg:.1f}℃")

# 분석 결과
# 가장 더웠던 날
highest_row = data[0]

for row in data:
    if float(row["최고기온"]) > float(highest_row["최고기온"]):
        highest_row = row

print(f"{highest_row['날짜']} {highest_row['도시']} {highest_row['최고기온']}℃")

# 일교차가 가장 큰 날
largest_gap = 0
largest_gap_day = None

for row in data:
    highest = float(row["최고기온"])
    lowest = float(row["최저기온"])

    gap = highest - lowest

    if gap > largest_gap:
        largest_gap = gap
        largest_gap_day = row


print(f"{largest_gap_day['날짜']} {largest_gap_day['도시']} {int(largest_gap)}℃")

