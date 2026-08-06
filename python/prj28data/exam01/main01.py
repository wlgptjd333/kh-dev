# 파일 읽기
import csv
from typing import Any

with open("sales.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    data = list(reader)
    # print(data[0])
# 전체 매출
total = 0
for row in data:
    total += int(row["단가"]) * int(row["수량"])

# 메뉴별 판매금액
qty_by_menu = {}
for row in data:
    # print(row["메뉴"], row["수량"])
    x = row["메뉴"]
    y = row["수량"]
    z = row["단가"]
    qty_by_menu[x] = qty_by_menu.get(x, 0) + int(y) * int(z)

# 카테고리별 매출
# 베스트 메뉴
# best_menu = ""
# max_value = -1
# for k, v in qty_by_menu.items():
#     if max_value < v:
#         max_value = v
#         best_menu = k
best_menu = max(qty_by_menu, key=qty_by_menu.get)

# 베스트 카테고리

# 월별 매출
sales_by_month = {}
for row in data:
    k = row["날짜"][0:7]
    금액 = int(row["수량"]) * int(row["단가"])
    sales_by_month[k] = sales_by_month.get(k, 0) + 금액

# 리포트 파일 저장
# print("total : ", total)
# print("qty_by_menu : ", qty_by_menu)
# print("best_menu : ", best_menu)
# print("sales_by_month", sales_by_month)

with open("report01.txt", "w", encoding="utf-8") as f:
    f.write("===== kh카페 매출 리포트 (2025 1분기)======\n\n")

    f.write(f"[전체 매출] {total:,}원\n\n")

    for k, v in qty_by_menu.items():
        f.write(f"{k}: {v}원\n")