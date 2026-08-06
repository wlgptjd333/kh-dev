# 언패킹

# a,b,*other,z= [1,2,3,4,5]
# dd = [*other]
# print(a,b)
# print(z)
# print(*other)
# print(type(dd))

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
a,b,c,*d = matrix
print(a)
print(b)
print(c)
print(d)