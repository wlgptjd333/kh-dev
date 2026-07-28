# 2차원 배열 => 행렬, 우리는 데이터 분석을 많이 할 것이기 때문에 행렬 분석이 중요함.
# 2차원 배열 잘 알아두기
a = list(range(3))
b = list(range(3))
c = list(range(3))

x = [a, b, c]

value = 10
for i in range(3):
    for j in range(3):
        x[i][j] = value
        value += 10

print(x)
