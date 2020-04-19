class Card:
    # Status 0  Hidden
    # Status 1  Shown

    def __init__(self):
        self.animal = None
        self.status = 0
        self.player = None

    def move(self, card):
        pass


class ElephantCard(Card):
    def __init__(self):
        self.animal = "Elephant"


class LionCard(Card):
    def __init__(self):
        self.animal = "Lion"


class TigerCard(Card):
    def __init__(self):
        self.animal = "Tiger"


class LeopardCard(Card):
    def __init__(self):
        self.animal = "Leopard"


class WolfCard(Card):
    def __init__(self):
        self.animal = "Wolf"


class dogCard(Card):
    def __init__(self):
        self.animal = "Dog"


class CatCard(Card):
    def __init__(self):
        self.animal = "Cat"


class RatCard(Card):
    def __init__(self):
        self.animal = "Rat"
