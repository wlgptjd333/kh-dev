class Turtle:
    def __init__(self):
        self.name = "turtle"
        self.hp = 110
        self.atk = 9

    def __repr__(self):
        return f"{self.name}, {self.hp}, {self.atk}"