import random

def play():
    print("\n===== 업다운 게임 =====")
    answer = random.randint(1, 100)
    attempts = 0
    
    while True:
        guess = int(input("1~100 사이의 숫자를 입력하세요 (종료: 0): "))
            
        if guess == 0:
            print("메인 메뉴로 돌아갑니다.")
            break
            
        attempts += 1
        
        # 제어문을 활용하여 판별
        if guess < answer:
            print("Up!\n")
        elif guess > answer:
            print("Down!\n")
        else:
            print(f"correct!!! 총 {attempts}번 만에 맞추셨습니다.\n")
            break