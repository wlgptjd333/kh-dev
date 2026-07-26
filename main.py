# - 제어문과 함수를 활용하여 **미니게임** 만들어보기 (3개 이상)
#     - main.py 에서 시작할 것
#     - game 폴더 내 xxxxx.py 파일을 만들어서 함수로 분리할 것
# - 필수로 만들어야할 게임
#     - 가위바위보
#     - 업다운
#     - 로또번호


from game import rps, up_down, lotto, reaction_time


while True:
    print("1. 가위바위보")
    print("2. 업다운")
    print("3. 로또번호")
    print("4. 반응속도 테스트")
    print("5. 게임 종료")
    choice = input("게임을 선택하세요 (1-5): ")

    if choice == '1':
        rps.play_rps()
    elif choice == '2':
        up_down.play_up_down()
    elif choice == '3':
        lotto.play_lotto()
    elif choice == '4':
        reaction_time.play_reaction_time()
    elif choice == '5':
        print("게임을 종료합니다.")
        break
    else:
        print("잘못된 입력입니다. 다시 선택해주세요.")