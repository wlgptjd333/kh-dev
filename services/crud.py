from data import db

# 1. 새 노트 작성
def create_note():
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
    db.next_id += 1  # 다음 노트를 위해 ID 번호 1 증가

# 2. 노트 목록 조회
def view_note_list():
    print("\n[ 전체 노트 목록 ]")
    if len(db.notes) == 0:
        print("등록된 노트가 없습니다.")
    else:
        for note in db.notes:
            print(f"[{note['id']}] {note['title']}")


# 3. 노트 읽기
def read_note():
    print("\n[ 노트 읽기 ]")
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

# 4. 노트 수정 (Update)
def update_note():
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
def delete_note():
    print("\n노트 삭제")
    search_id = input("삭제할 노트의 ID 번호를 입력하세요: ")

    if search_id.isdigit():
        search_id = int(search_id)
        found = False

        for note in db.notes:
            if note['id'] == search_id:
                db.notes.remove(note)
                print("노트가 성공적으로 삭제되었습니다!")
                found = True
                break

        if not found:
            print("해당 ID의 노트를 찾을 수 없습니다.")
    else:
        print("숫자로 입력해주세요.")

# 0. 프로그램 종료
def exit_program():
    print("\n미니 노트를 종료합니다. 안녕히 가세요!")

