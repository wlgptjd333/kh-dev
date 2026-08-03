# print_menu
from model.book import Book

book_list = []

def print_menu():
    print("------ menu ------")
    print("0. 프로그램 종료")
    print("1. 도서 등록")
    print("2. 도서 목록")
    print("3. 도서 조회")
    print("4. 도서 삭제")


# scan_user_input
def scan_user_input():
    num = int(input("메뉴 번호 : "))
    return num

# process
def process(num):
    match num:
        case 0:
            return False
        case 1:
            enroll_book()
        case 2:
            select_book_list()
        case 3:
            select_book_one()
        case 4:
            remove_book()

# 등록
def enroll_book():
    print("------ enroll book ------")
    t = input("title : ")
    a = input("author : ")
    book = Book(title=t, author=a)
    book_list.append(book)
    print("도서 등록 완료 !")

# 목록조회
def select_book_list():
    print("------ select book list ------")
    for i, book in enumerate(book_list):
        print(f"{i}. {book.title}")

# 상세조회
def select_book_one():
    print("----- 도서 상세 -----")
    num = int(input("num : "))
    book = book_list[num]
    print(book)

# 삭제
def remove_book():
    print("----- 도서 삭제 -----")
    num = int(input("num : "))
    del book_list[num]
    print("도서 삭제 완료 !")
