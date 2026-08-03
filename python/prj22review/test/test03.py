# def f01(x:str | int) -> str | float | None | list[int] | dict[str, int]:
#     print("f01 called~~")
#     print(x("f011"))
#     return "rrr"
#
# def f02(y) -> str:
#     print("f02 called~~")
#     print(y)
#     return y
#
# f01(f02)
#

# def f01(a, b="bbb", *x, y):
#     print("f01 called")
#     print(a, b, x, y)
#
#
# print(f01("ee", y= 0,))

# def a(x):
#     print("a called")
#     print(b())
#     return x
# def b():
#     print("b called")
#     return "b return"
#
# print(a(b()))


# 타입힌트
# 매개변수 , 리턴타입 , (+일반 변수에도 가능)
# def 함수이름(매개변수: 타입힌트) -> 리턴타입힌트
# x: 타입힌트 = 10

# e.g.
# def f01(a: int,b: float, c: str, d: bool) -> float:
#     return "hello"

# def f01(a: list, b: dict, c: tuple, d: set):
#     return "hello"

# def f01(a: list[int], b: dict[str, int], c: tuple[int, int], d: set[str]):
#     return "hello"

# 여러 타입 힌트 가능
# def f01(x: int | str):
#     return "hello"

# 값이 없을 때
# def f01(x: None) -> str | None:
#     return "hello"

# 기본값
# def f01(x="apple"):
#     return "hello"

# 변수에 함수를 담을 수 있다
# def f01():
#     return "hello"
# x = f01       # f01 뒤에 괄호 안붙어야됨 . 괄호 있으면 함수 호출.

# 가변인자 (매개변수 선언시에 순서 주의)
# def f01(*x , **y):  # x는 여러값을 받을 수 있음 , y는 딕셔너리 형태로 받을 수 있음
#     return "hello"
