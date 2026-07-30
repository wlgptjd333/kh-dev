from abc import abstractmethod, ABC


class Animal(ABC):
    def __init__(self, name, category, ):
        self.name = name
        self.category = category

    def __str__(self):
        return f'{self.name} {self.category}'

    @abstractmethod
    def bark(self):
        pass


class Dog(Animal):
    def __init__(self):
        super().__init__("강아지", "포유류")

    def bark(self):
        print("멍멍~~~")


class Cat(Animal):
    def __init__(self):
        super().__init__("고양이", "포유류")

    def bark(self):
        print("야옹~~~")


class Frog(Animal):
    def __init__(self):
        super().__init__("개구리", "양서류")

    def bark(self):
        print("개굴~~~")


class Dalamjwi(Animal):
    def __init__(self):
        super().__init__("다람쥐", "설치류")
