# n = 3
#
# table = []
# value = 1
#
# for row in range(n):
#     arr = []
#     for col in range(n):
#         if row % 2 == 0:
#             arr.append(value)
#         else:
#             arr.append(0)
#     table.append(arr)
#
# print(*table, sep='\n')

table = []

for j in range(5):
    arr = []
    for i in range(3):
        if j % 2 == 0:
            arr.append(1)
        else:
            arr.append(0)
    table.append(arr)

print(*table, sep='\n')
