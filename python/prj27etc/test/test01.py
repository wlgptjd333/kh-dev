# 컴프리헨션

matrix = [[1,2],[3,4]]

# -> [1,2,3,4]
# result = []
# for row in matrix:
#     for v in row:
#         result.append(v)

result = [v**2 for row in matrix for v in row]

print(result)