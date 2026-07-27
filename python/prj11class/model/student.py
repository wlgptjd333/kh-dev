class Student:
    def __init__(self, a, b):
        self.name = a
        self.score = b

    def __str__(self):
        return f"{self.name} {self.score} 입니다"