# lotto game

import random


def play_lotto():
    print("\n===== 로또 번호 맞추기 =====")
    while True:
        print("1~45 사이의 숫자 6개를 입력하세요 (종료: 0): ")
        user_numbers = []
        while len(user_numbers) < 6:
            num = int(input(f"{len(user_numbers) + 1}번째 번호: "))
            if num == 0:
                print("메인 메뉴로 돌아갑니다.")
                return
            elif num not in range(1, 46) or num in user_numbers:
                print("잘못된 입력입니다. 다시 입력해주세요.")
                continue
            else:
                user_numbers.append(num)
                
        computer_numbers = random.sample(range(1, 46), 6)
        print(f"사용자 번호: {sorted(user_numbers)}")
        print(f"컴퓨터 번호: {sorted(computer_numbers)}")
        matches = 0
        for num in user_numbers:
            if num in computer_numbers:
                matches += 1
        print(f"맞춘 개수: {matches}\n")
