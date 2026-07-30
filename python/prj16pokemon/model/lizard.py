class Lizard:
    def __init__(self):
        self.name = "lizard"
        self.hp = 90
        self.atk = 11

    def __repr__(self):
        return f"{self.name}, {self.hp}, {self.atk}"