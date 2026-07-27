def solution(a, b):
    return max(int(f"{a}{b}"), int(f"{b}{a}"))

print(solution(88, 9))