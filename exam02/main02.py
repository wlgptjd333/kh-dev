import csv
# 대출일,도서명,분야,대출자유형,대출일수
# 2025-03-01,부의 추월차선,경제,학생,7
# 2025-03-01,파이썬 첫걸음,IT,학생,14

with open("loans.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    data = list(reader)
    print(data[0])
# # 전체 매출
# total = 0
# for row in data:
#     total += int(row["대출일"])