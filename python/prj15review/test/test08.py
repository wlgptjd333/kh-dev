# 3*3
names = ["심원용", "심투용", "심삼용"]
subjects = ["수학", "영어", "과학"]

row_number = 3
col_number = 3
table = []

for i in range(row_number):
    arr = []
    for j in range(col_number):
        arr.append(0)
    table.append(arr)

#성적 입력
table[0][0] = 40
table[0][1] = 90
table[0][2] = 80
table[1][0] = 10
table[1][1] = 20
table[1][2] = 30
table[2][0] = 70
table[2][1] = 60
table[2][2] = 50

for i in table:
    print(i)


# 총점이 제일 높은 학생 이름, 총점 출력
total_list = []

for i in range(3):
    total = 0
    for score in table[i]:
        total += score
    total_list.append(total)

print(f"total_list: {total_list}")

idx = -1
top = 0
for i in range(3):
    if top < total_list[i]:
        top = total_list[i]
        idx = i

print(f"top: {top}, idx: {idx}, name: {names[idx]}")