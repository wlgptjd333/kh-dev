from unittest import case

from services.crud import (create_note, view_note_list, read_note,
                           delete_note, exit_program, update_note)


def display_menu():
    print(" 미니 노트에 오신 것을 환영합니다!\n")

    while True:
        print("\n" + "=" * 50)
        print("1. 새 노트 작성(C)  2. 노트 목록(R)  3. 노트 읽기(R)")
        print("4. 노트 수정(U)     5. 노트 삭제(D)  0. 종료")
        print("=" * 50)

        choice = int(input("메뉴를 선택하세요: "))

        match choice:
            case 1:
                create_note()
            case 2:
                view_note_list()
            case 3:
                read_note()
            case 4:
                update_note()
            case 5:
                delete_note()
            case 0:
                exit_program()
                break
            case _:
                print("\n 잘못된 입력입니다. 메뉴 범위에서 선택해주세요.")
                continue
