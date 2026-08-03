# - 파이썬을 활용하여 **관리 프로그램** 만들어보기
#     - main.py 에서 시작할 것
#     - 오늘 수업내용 도서관리프로그램 참고
# - 필수로 만들어야할 기능
#     - 등록
#     - 목록조회
#     - 상세조회
#     - 삭제
#     - 반복문 적용

### 학원 홈페이지에 제출하기

# - 제목 : **[파이썬] CRUD_홍길동**
# - ~~첨부파일 : X~~
# - 내용 : 깃허브 링크

# main.py
from data import db  # data 폴더 안의 db.py를 불러옵니다.


def main():
    print(" 미니 노트에 오신 것을 환영합니다!\n")

    while True:
        print("\n" + "=" * 50)
        print("1. 새 노트 작성(C)  2. 노트 목록(R)  3. 노트 읽기(R)")
        print("4. 노트 수정(U)     5. 노트 삭제(D)  0. 종료")
        print("=" * 50)

        choice = input("메뉴를 선택하세요: ")

        # 1. 새 노트 작성
        if choice == '1':
            print("\n[ 새 노트 작성 ]")
            title = input("제목: ")
            content = input("내용: ")

            new_note = {
                "id": db.next_id,
                "title": title,
                "content": content
            }
            db.notes.append(new_note)

            print(f"{title} 노트가 저장되었습니다!")
            db.next_id += 1  # 다음 아이템을 위해 ID 번호 1 증가

        # 2. 노트 목록 조회
        elif choice == '2':
            print("\n[ 전체 노트 목록 ]")
            if len(db.notes) == 0:
                print("등록된 노트가 없습니다.")
            else:
                for note in db.notes:
                    print(f"[{note['id']}] {note['title']}")

            print(f"현재 총 {len(db.notes)}개의 노트가 있습니다.")

        # 3. 노트 상세 읽기 (Read - Detail)
        elif choice == '3':
            print("\n[ 노트 상세 읽기 ]")
            search_id = input("읽을 노트의 ID 번호를 입력하세요: ")

            if search_id.isdigit():
                search_id = int(search_id)
                found = False

                for note in db.notes:
                    if note['id'] == search_id:
                        print("\n" + "-" * 30)
                        print(f"제목: {note['title']}")
                        print(f"내용: {note['content']}")
                        print("-" * 30)
                        found = True
                        break

                if not found:
                    print("해당 ID의 노트를 찾을 수 없습니다.")
            else:
                print("숫자로 입력해주세요.")

        # 4. 노트 수정 (Update) - 새롭게 추가된 기능!
        elif choice == '4':
            print("\n[ 노트 수정 ]")
            search_id = input("수정할 노트의 ID 번호를 입력하세요: ")

            if search_id.isdigit():
                search_id = int(search_id)
                found = False

                for note in db.notes:
                    if note['id'] == search_id:
                        print(f"현재 제목: {note['title']}")
                        new_title = input("새 제목 (변경하지 않으려면 그냥 엔터): ")
                        if new_title != "":
                            note['title'] = new_title

                        print(f"현재 내용: {note['content']}")
                        new_content = input("새 내용 (변경하지 않으려면 그냥 엔터): ")
                        if new_content != "":
                            note['content'] = new_content

                        print("노트가 수정되었습니다!")
                        found = True
                        break

                if not found:
                    print("해당 ID의 노트를 찾을 수 없습니다.")
            else:
                print("숫자로 입력해주세요.")

        # 5. 노트 삭제 (Delete)
        elif choice == '5':
            print("\n노트 삭제")
            search_id = input("삭제할 노트의 ID 번호를 입력하세요: ")

            if search_id.isdigit():
                search_id = int(search_id)
                found = False

                for note in db.notes:
                    if note['id'] == search_id:
                        db.notes.remove(note)  # 리스트에서 해당 딕셔너리 삭제
                        print("노트가 성공적으로 삭제되었습니다!")
                        found = True
                        break

                if not found:
                    print("해당 ID의 노트를 찾을 수 없습니다.")
            else:
                print("숫자로 입력해주세요.")

        # 0. 프로그램 종료
        elif choice == '0':
            print("\n미니 노트를 종료합니다. 안녕히 가세요!")
            break

        else:
            print("\n 잘못된 입력입니다. 메뉴 범위에서 선택해주세요.")


# 프로그램 시작점
if __name__ == "__main__":
    main()
