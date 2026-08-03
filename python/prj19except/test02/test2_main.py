def f01():
    try:
        print(f02())
    except Exception as e:
        print("오류오류발생", e)
    print("f01 finish !!!")


def f02():
    print("f02 called~~~~~")
    raise Exception(f03())
    # f03()
    # print("f02 finish !!!")


def f03():
    print("f03 called~~~~~")
    print("f03 finish !!!")


f01()
