a = 2
b= 92

def solution(a, b):
    if int(str(a)+str(b))>=(2*a*b):
        return int(str(a)+str(b))
    else:
        return (2*a*b)

print(solution(a, b))