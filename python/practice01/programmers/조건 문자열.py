ineq = "<"
eq = "="
n = 20
m = 50

def solution(ineq, eq, n, m):
    if (eq == "=" and n == m) or (ineq == ">" and n > m) or (ineq == "<" and n < m):
        return 1
    else:
        return 0
