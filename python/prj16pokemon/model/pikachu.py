class Pikachu:
    def __init__(self):
        self.name = "Pikachu"
        self.hp = 100
        self.atk = 10

    def __repr__(self):
        return f"{self.name}, {self.hp}, {self.atk}"