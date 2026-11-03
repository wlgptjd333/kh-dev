# 가위바위보 게임
import random

def play_rps():
    options = ['가위', '바위', '보']
    print("\n===== 가위바위보 게임 =====")
    
    while True:
        user = input("가위, 바위, 보 중 하나를 입력하세요 (종료: 0): ")
        
        if user == '0':
            print("메인 메뉴로 돌아갑니다.")
            break
            
        if user not in options:
            print("잘못된 입력입니다. 다시 입력해주세요.")
            continue
            
        com = random.choice(options)
        print(f"컴퓨터: {com}")
        
        # 제어문을 활용한 승패 판별
        if user == com:
            print("결과: 비겼습니다!\n")
        elif (user == '가위' and com == '보') or \
             (user == '바위' and com == '가위') or \
             (user == '보' and com == '바위'):
            print("결과: 이겼습니다!\n")
        else:
            print("결과: 졌습니다!\n")