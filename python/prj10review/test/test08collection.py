# list, dictionary, set, tuple
def func01():
    a = [10, 20, 30, 40, 50]
    a.append(100)
    a.append(200)
    a.insert(2, 777)
    print(a)


# a[0] = 123
# print(a)
# result = a.sort()
# print(result)
# b = a
# print(b)

def func02():
    print("----- dict -----")
    person = {"name": "hong", "age": 18, "blood": "A"}
    person["age"] += 1111
    print(person["name"])
    print(person["age"])
    print(person["blood"])
    person.get("name")
    print(person.get("mbti", "음성"))
    print("hong" in person.values())
    print(("age", 1129) in person.items())


def func02_1():
    x = {
        "p1": {"name": "철수", "age": 20},
        "p2": {"name": "영희", "age": 21},
        "p3": {"name": "미영", "age": 30},
    }
    print(x)


def func03():
    print("----- set -----")
    x = {10, 20, 30}
    y = {20, 30, 40}
    print(sorted(x | y))

def func04():
    x = (10, 20, 30)
    print(x[0])

func04()

