import json

from book.model.book import Book

def print_menu() -> None:
    print("---------- MENU ----------")
    print("0. exit")
    print("1. insert")
    print("2. select list")
    print("3. select one")
    print("4. edit")
    print("5. remove")

def scan_menu_num() -> int:
    num = int(input("menu num: "))
    return num


def insert():
    book_list = select_list()
    with open("book_data.json", "w", encoding="utf-8") as f:
        t = input("title : ")
        a = input("author : ")
        p = input("price : ")
        book = Book(t, a, p)
        book_dict = book.to_dict()
        book_list.append(book_dict)
        json.dump(book_list, f, ensure_ascii=False, indent=2)


def select_list():
    with open("book_data.json", "r", encoding="utf-8") as f:
        book_list = json.load(f)
    return book_list

def print_book_list(book_list: list) -> None:
        for book_dict in book_list:
            book = Book.from_dict(book_dict)
            print(book)

def select_one():
    pass


def edit():
    print("edit")


def remove():
    print("remove")


def process(num: int) -> None:
    match num:
        case 1:
            insert()
        case 2:
            book_list = select_list()
            print_book_list(book_list)
        case 3:
            select_one()
        case 4:
            edit()
        case 5:
            remove()


def program_start():
    while True:
        try:
            print_menu()
            num = scan_menu_num()
            if num == 0: break
            process(num)
        except Exception as e:
            print("[예외 발생]", e)
            print("그치만 안멈출거임")


