
class Book:
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    def __str__(self):
        return f"{self.title} by {self.author} ({self.price}원)"


    def to_dict(self) -> dict:
        return {"title": self.title, "author": self.author, "price": self.price}

    @staticmethod
    def from_dict(dict_data) -> Book:
        return Book(dict_data["title"], dict_data["author"], dict_data["price"])