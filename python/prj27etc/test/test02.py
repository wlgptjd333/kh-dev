# 컴프리헨션

# result = []
# for x in range(10):
#     if x % 2 == 0:
#         result.append("짝")
#     else:
#         result.append("홀")

result = ["짝" if n % 2 == 0 else "홀" for n in range(10)]

print(result)