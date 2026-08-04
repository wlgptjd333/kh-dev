n = 7

def solution(n):
    result = 0
    if n % 2 == 1:
        for i in range(n, 0, -2):
            result += i
        return result
    else:
        for i in range(n, 0, -2):
            result += (i*i)
        return result

print(solution(n))