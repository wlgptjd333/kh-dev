class Book:
    def __init__(self, t, p):
        self.title = t
        self.price = p

    def to_dict(self):
        return {
            "title": self.title,
            "price": self.price
        }

    @staticmethod
    def from_dict(d):
        return Book(d["title"], d["price"])