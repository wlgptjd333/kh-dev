def check_pw_validation(pw):
    if len(pw) < 4:
        raise Exception("pw is too short")
    if len(pw) > 8:
        raise Exception("pw is too long")

def join():
    print("join called ~~~")
    member_id = input("id : ")
    member_pw = input("pw : ")

    check_pw_validation(member_pw)

    print("join finish ~~~")

