# row(행), col(열) 사용자한테 입력받아서
# 2차원 배열 생성하기 (값은 1부터 시작해서 1씩 증가)

row_number = int(input("행: "))
col_number = int(input("열: "))

arr = []
value = 1

for row in range(row_number):
    x = []
    for col in range(col_number):
        x. append(value)
        value += 1
    arr.append(x)

for temp in arr:
    print(arr)