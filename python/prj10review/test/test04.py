# 4글자 ~ 12글자
# 4개 연속된 값 ㄴㄴ
# "@" 또는 "!" 를 포함해야됨
from operator import contains

def is_valid_password(pw):
    if len(pw) < 4:
        return False
    elif len(pw) > 12:
        return False
    elif pw[0] == pw[1] == pw[2] == pw[3] :
        return False
    elif not (contains(pw,"!") or contains(pw,"@")) :
        return False
    else:
        return True

def is_valid_password(pw):
    if len(pw) < 4:
        return False

    if len(pw) > 12:
        return False

    if pw[0] == pw[1] == pw[2] == pw[3]:
        return False

    if not (contains(pw, "!") or contains(pw, "@")):
        return False

    return True
