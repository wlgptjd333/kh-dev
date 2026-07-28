from service.book_service import *


# 메뉴판
def print_menu():
    print("0. 프로그램 종료")
    print("1. 도서 등록")
    print("2. 도서 목록조회")
    print("3. 도서 상세조회")
    print("4. 도서 삭제")


# 입력받기
def scan_menu_num():
    menu_num = input("메뉴 번호 : ")
    return menu_num


# 작업하기
def process(menu_num):
    match menu_num:
        case "0":
            return True
        case "1":
            enroll_book()
        case "2":
            print_book_list()
        case "3":
            print_book_one_by_number()
        case "4":
            delete_book_one_by_number()
        case _:
            print("잘못된 입력입니다")
