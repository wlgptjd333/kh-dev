n = 3

table = []
value = 1

for row in range(n):
    arr = []
    for col in range(n):
        if col == row:
            arr.append(value)
        else:
            arr.append(0)
    table.append(arr)

print(*table, sep='\n')