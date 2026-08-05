import csv

#대출일,도서명,분야,대출자유형,대출일수

with open("loans.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    data = list(reader)

if data:
    print(data[0])
else:
    print("데이터가 없습니다.")

# 총 대출 건수
total = len(data)
print(f"[총 대출 건수] {total}건")

# 평균 대출일수
avg_day = 0
total_day = 0
for row in data:
    total_day += int(row["대출일수"])
    avg_day = total_day / total
print(f"[평균 대출일수] {round(avg_day, 1)}일")

# 분야별 대출 건수
field_count = {}

for row in data:
    field = row["분야"]

    if field in field_count:
        field_count[field] += 1
    else:
        field_count[field] = 1

for field, count in field_count.items():
    print(f"{field}: {count}건")

# 대출자 유형별
user_type_count = {}

for row in data:
    type = row["대출자유형"]

    if type in user_type_count:
        user_type_count[type] += 1
    else:
        user_type_count[type] = 1

for type, count in user_type_count.items():
    print(f"{type}: {count}")

# 월별 대출 건수
monthly_count = {}

for row in data:
    monthly = row["대출일"][0:7]

    if monthly in monthly_count:
        monthly_count[monthly] += 1
    else:
        monthly_count[monthly] = 1

for month, count in monthly_count.items():
    print(f"{month}: {count}")

# 분석 결과
# 최다 대출 도서
borrow_book = {}

for row in data:
    book = row["도서명"]

    if book in borrow_book:
        borrow_book[book] += 1
    else:
        borrow_book[book] = 1

for book, count in borrow_book.items():
    print(f"{book}: {count}")

most_book = (max(borrow_book, key=borrow_book.get))
most_book_num = borrow_book[most_book]

print(most_book_num, most_book)
# 인기 분야 1위


# 결과를 파일로 저장
with open("report02.txt", "w", encoding="utf-8") as out:
    out.write(f"[총 대출 건수] {total}건\n")