x = []
num = 0
for i in range(1,4):
    y = []
    for j in range(3):
        num += 10
        y.append(num)
    x.append(y)
print(x)