from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


class Book(BaseModel):
    title: str
    price: int


@app.post("/book")
def create_book(book: Book):
    print(book)
    if book.price < 0:
        return "bad price"
    return "goooooooooooooood"


@app.post("/hello")
def hello(title: str = Form(), price: int = Form(0)):
    print(f"{title} / {price}")
    print(type(title))
    print(type(price))
    print("hello called ~~~")
    return {"message": "hello called ~~~", "title": title, "price": price}