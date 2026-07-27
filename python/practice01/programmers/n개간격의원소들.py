def solution(num_list, n):
    answer = [*num_list[::n]]
    return answer

s = solution([4, 2, 6, 1, 7, 6], 2)
print(*s)