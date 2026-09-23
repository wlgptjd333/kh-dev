from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


class Order(BaseModel):
    menu: str
    count: int


class Signup(BaseModel):
    email: str
    pw: str
    pw_check: str


class Calc(BaseModel):
    a: int
    b: int
    op: str


# 문제1
@app.post("/book")
def book(title: str = Form(), price: int = Form()):
    if price < 10000:
        return "fail..."
    return "goooooooooooooood!!!"


@app.post("/login")
def login(id: str = Form(), pw: str = Form()):
    if id == "admin":
        if pw == "1234":
            return "login ok"
    return "login fail..."


@app.get("/age")
def age(name: str, age: int):
    if age > 20:
        return f"{name}님은 성인입니다"
    return f"{name}님은 미성년자입니다"


@app.get("/score")
def score(kor: int = Form(), eng: int = Form(), math: int = Form()):
    if (kor + eng + math) / 3 >= 60:
        return "pass"
    return "fail..."


@app.post("/order")
def order(order: Order):
    if order.count >= 1 and order.count <= 10:
        return f"{order.menu} {order.count}개 주문 완료"
    return "fail... 주문 수량 오류"


@app.get("/even")
def even(num: int):
    if num % 2 == 0:
        return "even"
    return "odd"


@app.post("/singup")
def signup(signup: Signup):
    if "@" not in signup.email:
        return "email error..."
    if signup.pw != signup.pw_check:
        return "password mismatch..."
    return "singup success!"


@app.get("/grade")
def grade(score: int = Form()):
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    return "f"


@app.get("/product")
def product(name: str = Form(), price: int = Form(), stock: int = Form()):
    if stock < 0:
        return "품절..."

    if price < 0:
        return "가격 오류..."

    return "등록 완료"


@app.post("/calc")
def calc(calc: Calc):
    if calc.b == 0 and calc.op == "/":
        return "0으로 나눌 수 없음"
    if calc.op == "+":
        return calc.a + calc.b
    elif calc.op == "-":
        return calc.a - calc.b
    elif calc.op == "*":
        return calc.a * calc.b
    elif calc.op == "/":
        return calc.a / calc.b

    return "연산자 오류..."
