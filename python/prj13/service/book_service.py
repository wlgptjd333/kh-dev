from model.book import Book

book_list = []


# 등록하기
def enroll_book():
    print("\n----- 도서 등록 -----")
    title = input("도서 제목 : ")
    price = input("도서 가격 : ")
    book_list.append(Book(title, price))
    print("등록 완료 !")


# 목록출력
def print_book_list():
    print("\n----- 도서 목록 -----")
    print("번호 | 제목")
    for idx, b in enumerate(book_list):
        print(f"{idx + 1} | {b.title}")


# 상세조회 (도서 번호 이용해서 조회)
def print_book_one_by_number():
    print("\n----- 도서 상세 -----")
    book_num = int(input("조회할 도서 번호 : "))
    b = book_list[book_num - 1]
    print(b)


# 삭제하기 (도서 번호 이용해서 삭제)
def delete_book_one_by_number():
    print("\n----- 도서 삭제 -----")
    book_num = int(input("삭제할 도서 번호 : "))
    del book_list[book_num - 1]
    print("삭제 완료 !")
