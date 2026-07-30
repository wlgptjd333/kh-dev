class Pokemon:
    def __init__(self, a, b, c):
        self.name = a
        self.hp = b
        self.atk = c

    def __repr__(self):
        return f"{self.name}, {self.hp}, {self.atk}"
