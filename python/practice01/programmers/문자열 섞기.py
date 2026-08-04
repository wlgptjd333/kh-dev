str1 = "Hello"
str2 = "Hoyee"


def solution(str1, str2):
    answer = ''
    for i in range(len(str1)):
        answer += str1[i] + str2[i]
    return answer


print(solution(str1, str2))
