# match
# 1 ~ 12월의 말일 출력하기(윤년 제외)

month = input("month : ")

match month:
    case "1" | "3" | "5" | "7" | "8" | "10" | "12":
        print(31)
    case "2":
        print(28)
    case "4" | "6" | "9" | "12":
        print(30)
    case _:
        print("그런 month는 없습니다,")
