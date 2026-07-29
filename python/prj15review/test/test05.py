n = 3

table = []
value = 1

for row in range(n):
    arr = []
    for col in range(n):
        arr.append(value)
    table.append(arr)

print(*table, sep='\n')