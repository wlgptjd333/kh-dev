class Book:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __str__(self):
        print("str 함수 호출")
        return f"[Book] title: {self.title}, price: {self.price}"

    def __repr__(self):
        print("repr 함수 호출")
        return f"[Book] title: {self.title}, price: {self.price}"