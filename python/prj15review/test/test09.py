# 3*3

names = ["심원용", "심투용", "심삼용"]
subjects = ["수학", "영어", "과학"]

row_number = 3
col_number = 3

table = [[0] * col_number for _ in range(row_number)]

# 성적 입력
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

# 문제
students_total_list = [0, 0, 0]
subjects_total_list = [0, 0, 0]
subjects_avg_list = []
students_avg_list = []
top_score_list = []
top_student_list = []

# 과목별 평균
for i in range(row_number):
    for j in range(col_number):
        subjects_total_list[j] += table[i][j]

for i in range(row_number):
    subjects_avg_list.append(subjects_total_list[i] / row_number)

print(f"\n과목별 총점: {subjects_total_list}")
print(f"과목별 평균: {subjects_avg_list}")

# 학생별 총점과 평균
for i in range(row_number):
    for j in range(col_number):
        students_total_list[i] += table[i][j]

for j in range(col_number):
    students_avg_list.append(students_total_list[j] / col_number)

print(f"\n학생별 총점: {students_total_list}")
print(f"학생별 평균: {students_avg_list}")

# 과목별 최고 점수와 해당 학생 이름
for i in range(row_number):
    top_idx = -1
    top = -1
    for j in range(col_number):
        if top < table[j][i]:
            top = table[j][i]
            top_idx = j
    top_student_list.append(names[top_idx])
    top_score_list.append(top)

for i in range(3):
    print(f"{subjects[i]} 최고 점수: {top_score_list[i]} |"
          f" 학생 이름: {top_student_list[i]}")

# 총점 최고득점자와 최저득점자 이름
top_score_student = [""]
top_score = 0
worst_score_student = [""]
worst_score = float('inf')
for i in range(row_number):
    if top_score < students_total_list[i]:
        top_score = students_total_list[i]
        top_score_student[0] = (names[i])
    if worst_score > students_total_list[i]:
        worst_score = students_total_list[i]
        worst_score_student[0] = (names[i])
print(f"\n최고의 학생: {top_score_student} | 총점: {top_score}")
print(f"아쉬운 학생: {worst_score_student} | 총점: {worst_score}")

# 평균 미만 출력 (평균 60점 미만)
low_avg_students = []

for i in range(row_number):
    if 60 > students_avg_list[i]:
        low_avg_students.append(names[i])

print(f"\n평균 미만인 학생: {low_avg_students}")

# 과락자 출력 (1과목이라도 40점 이하인 경우)
f_students = []
for i in range(row_number):
    for j in range(col_number):
        if 40 >= table[i][j]:
            f_students.append(names[i])
            break

print(f"과락자: {f_students}")
