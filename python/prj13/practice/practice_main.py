from practice.book import Book
#도서관리 프로그램 만들기
book_list = []
#메뉴 프린트
print("-----도서 관리 프로그램-----")

def print_menu():
    print("1번 : 도서 추가")
    print("2번 : 도서 삭제")
    print("3번 : 도서 조회")
    print("4번 : 도서 상세조회")
    print("0번 : 프로그램 종료")
#메뉴 선택
def select_menu():
    num = int(input("\n번호 선택(0~4) : "))
    return num
#도서 추가
def enroll_book():
    print("\n----- 도서 추가 -----")
    title = input("제목 : ")
    author = input("저자 : ")
    price = input("가격 : ")
    book_list.append(Book(title, author, price))
#도서 삭제
def delete_book():
    print("\n----- 도서 삭제 -----")
    num = int(input("삭제할 도서 번호 : "))
    del book_list[num-1]
#도서 조회
def ask_book():
    print("\n----- 도서 조회 -----")
    num = int(input("조회할 도서 번호 : "))
    print(book_list[num-1])
#도서 상세조회

#메뉴 실행
def process_book():

    match select_menu():
        case 1:
            enroll_book()
        case 2:
            delete_book()
        case 3:
            ask_book()
        case 4:
            pass
        case 0:
            True

while True:
    print_menu()
    process_book()