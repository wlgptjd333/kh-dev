import json

from book import Book


def write_to_file():
    with open("output.txt", "w", encoding="utf-8") as f:
        title = input("title : ")
        price = int(input("price : "))
        book = Book(title, price)
        json.dump(book.to_dict(), f, ensure_ascii=False, indent=4)


def read_from_file():
    with open("output.txt", "r", encoding="utf-8") as f:
        d = json.load(f)
        print(d)
        book = Book.from_dict(d)
        print(type(d))
        print(book.title)
        print(type(book))

# with open("data.txt", "r", encoding="utf-8") as f:
#     for x in f:
#         print(x.strip())

while True:
    print("0. exit")
    print("1. write")
    print("2. read")
    num = int(input("메뉴 번호"))
    match num:
        case 0:
            break
        case 1:
            write_to_file()
        case 2:
            read_from_file()
