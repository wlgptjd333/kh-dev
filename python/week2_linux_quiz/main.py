import random

import quiz

# 리눅스 명령어 퀴즈 프로그램 만들기
'''
- **리눅스 명령어 퀴즈 프로그램 만들기**
- 조건문,반복문,리스트 사용할 것
- 문제는 최소 5문제 이상 준비할 것
(문제로는 명령어의 설명을 주고, 정답은 명령어를 맞히도록)
- 5문제 중 랜덤으로 3문제 뽑아서 출제할 것
- 문제 유형은 모두 주관식으로 할 것
- 정답은 대소문자 구분없이 정답처리 가능하도록 할 것
- 정답을 못 맞추면, 바로 정답을 알려줄 것
- 마지막에 총 몇문제 맞추었는지 알려줄 것
- 맞춘 문제 수에 따라 등급 출력 (A,B,C,F)
- 게임 종료 후 재시도 할 수 있게 만들어줄 것
- 유저 입력으로 게임을 그만할 수 있게 만들어줄 것 (프로세스 종료)
'''

is_play = ""

while is_play != "n":
    # k = int(input(f"{len(quiz.question_list)}문제 중에 몇 문제 푸시겠습니까?"))
    k = 3
    print("리눅스 3문제를 랜덤으로 출제합니다. 정답 개수에 따라 등급이 달라집니다.\n")
    question_number = random.sample(range(len(quiz.quiz_data)), k)
    correct_number = 0

    for i in question_number:
        current_quiz = quiz.quiz_data[i]
        print(current_quiz["question"])
        answer = input().lower()

        if answer == current_quiz["answer"]:
            print(f"{i + 1}번 문제 정답입니다!\n")
            correct_number += 1
        else:
            print(f"{i + 1}번 문제의 정답은 {current_quiz["answer"]}입니다. 아쉽네요\n")

    if correct_number == 0:
        print("F등급입니다!\n")
    elif correct_number == 1:
        print("C등급입니다!!\n")
    elif correct_number == 2:
        print("B등급입니다!!!\n")
    else:
        print("A등급입니다!!!!! 대단합니다! 정답을 모두 맞췄습니다!\n")

    is_play = input(("게임을 계속 하시겠습니까? Y/n\n"))
    print()

print("게임을 종료합니다.")
