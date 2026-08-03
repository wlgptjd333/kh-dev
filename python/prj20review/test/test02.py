table = [
    [10, 20, 30],
    [40, 50, 60],
    [70, 80, 90]
]

# +1
for i in range(len(table)):
    for j in range(len(table[i])):
        table[i][j] += 1  # 위치를 직접 지정해서 1씩 증가시킴

print(table)

# 행별 합계를 출력
row_list = []

for i in table:
    total = 0
    total = sum(i)
    print(total)
    row_list.append(total)

print(row_list)
# 열별 합계 출력
col_list = []

for i in range(len(table)):
    col = 0
    for j in range(len(table[i])):
        col += table[j][i]
    col_list.append(col)

print(col_list)

# 결측치를 찾고, 해당 행 삭제
table = [
    [10, 20, 30],
    [40, 50, None],
    [70, 80, 90]
]

for i in range(len(table) -1, -1, -1):
    if None in table[i]:
        del table[i]

print(table)