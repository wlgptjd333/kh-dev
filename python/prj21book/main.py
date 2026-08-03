# 도서 관리
from model.book_manager import process, print_menu, scan_user_input

print("===== 도서 관리 프로그램 =====")

while True:
    try:
        print_menu()
        num = scan_user_input()
        process(num)
    except Exception as e:
        print(e)

