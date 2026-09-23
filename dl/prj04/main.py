from fastapi import FastAPI, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse, HTMLResponse, FileResponse

app = FastAPI()


class Person():
    def __init__(self, name, age):
        self.name = name
        self.age = age


@app.get("/f1")
def f01():
    print("f01 called ...")
    x = Person("hongggg", 18)
    return RedirectResponse("/f2")


@app.get("/f2")
def f02():
    return {"message": "f2 무사히 도착했당!"}


@app.get("/f3")
def f03():
    print("f3 called ...")
    s = "<h1>hello world</h1>"
    return HTMLResponse(s)


@app.get("/f4")
def f04():
    print("f4 called ...")
    return Response(
        status_code=200,
        headers={
            "atk": "150",
            "speed": "200",
            "nickname" : "hong",
        },
        media_type="text/plain",
        content="여긴 한국어 ㄱㅊ",
    )

@app.get("/f5")
def f05():
    print("f5 called ...")
    return JSONResponse(
        status_code=200,
        headers={
        "snack": "sae woo ggang"
        },
        media_type="application/json",
        content={
            "x" : 100,
            "y" : 200,
        },
    )

@app.get("/f6")
def f06():
    print("f6 called ...")
    x = Person("hongggg", 18)
    return JSONResponse(
        status_code=200,
        headers={},
        content=jsonable_encoder(x)
    )

@app.get("/f7")
def f07():
    print("f7 called ...")
    return FileResponse("test03.png")

@app.get("/f8")
def f8(nick:str = "GUEST"):
    print("f8 called ...")
    s = f'''
    <h1>{nick}님 환영합니다.</h1>
    '''
    return HTMLResponse(s)