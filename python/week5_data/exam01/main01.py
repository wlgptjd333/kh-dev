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

# 메뉴별 판매량
qty_by_menu2 = {}
for row in data:
    x = row["메뉴"]
    y = row["수량"]
    qty_by_menu2[x] = qty_by_menu2.get(x, 0) + int(y)

# 카테고리별 매출
qty_by_cate = {}
sales_by_cate = {}
for row in data:
    x = row["카테고리"]
    y = row["수량"]
    z = row["단가"]
    sales_by_cate[x] = sales_by_cate.get(x, 0) + int(y) * int(z)
    qty_by_cate[x] = qty_by_cate.get(x, 0) + int(y)
# 베스트 메뉴
# best_menu = ""
# max_value = -1
# for k, v in qty_by_menu.items():
#     if max_value < v:
#         max_value = v
#         best_menu = k
best_menu_cate = max(sales_by_cate, key=sales_by_cate.get)
best_menu_qty = max(qty_by_menu2, key=qty_by_menu2.get)
best_menu_qty_num = qty_by_menu2.get(best_menu_qty)
best_menu = max(qty_by_menu, key=qty_by_menu2.get)
best_menu_cate_sales = (sales_by_cate.get(best_menu_cate))
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
# print("best_menu : ", best_menu2)
# print("sales_by_month", sales_by_month)

with open("report01.txt", "w", encoding="utf-8") as f:
    f.write("=== 파이빈 카페 매출 리포트 (2025.01 ~ 03) ===\n\n")

    f.write(f"[전체 매출] {total:,}원\n\n")

    f.write("[메뉴별 판매량]\n")
    for k, v in qty_by_menu2.items():
        f.write(f"{k}: {v}잔\n")

    f.write("\n[카테고리별 매출]\n")
    for k, v in sales_by_cate.items():
        f.write(f"{k}: {v:,}원\n")

    f.write("\n[월별 매출]\n")
    for k, v in sales_by_month.items():
        f.write(f"{k}: {v:,}원\n")

    f.write("\n[분석 결과]\n")
    f.write(f"가장 많이 팔린 메뉴: {best_menu_qty} ({best_menu_qty_num}잔)\n")
    f.write(f"매출 1위 카테고리: {best_menu_cate}({best_menu_cate_sales:,}원)")