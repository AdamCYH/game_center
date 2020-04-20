class PieceCollection:
    def __init__(self):
        self.cards = None


class AnimalChessPieceCollection(PieceCollection):
    def __init__(self, player):
        super().__init__()
        self.cards = [ElephantCard(player),
                      LionCard(player),
                      TigerCard(player),
                      LeopardCard(player),
                      WolfCard(player),
                      DogCard(player),
                      CatCard(player),
                      RatCard(player)]


class Piece:
    # Status 0  Hidden
    # Status 1  Shown

    def __init__(self, player):
        self.animal = None
        self.status = 0
        self.player = player
        self.x = None
        self.y = None

    def flip(self):
        return

    def move(self):
        return

    def set_player(self, player):
        self.player = player

    def __str__(self):
        return str(self.player) + ":" + self.animal

    def __repr__(self):
        return str(self.player) + ":" + self.animal


class ElephantCard(Piece):
    def __init__(self, player):
        super().__init__(player)
        self.animal = "Elephant"
        self.index = 7


class LionCard(Piece):
    def __init__(self, player):
        super().__init__(player)
        self.animal = "Lion"
        self.index = 6


class TigerCard(Piece):
    def __init__(self, player):
        super().__init__(player)
        self.animal = "Tiger"
        self.index = 5


class LeopardCard(Piece):
    def __init__(self, player):
        super().__init__(player)
        self.animal = "Leopard"
        self.index = 4


class WolfCard(Piece):
    def __init__(self, player):
        super().__init__(player)
        self.animal = "Wolf"
        self.index = 3


class DogCard(Piece):
    def __init__(self, player):
        super().__init__(player)
        self.animal = "Dog"
        self.index = 2


class CatCard(Piece):
    def __init__(self, player):
        super().__init__(player)
        self.animal = "Cat"
        self.index = 1


class RatCard(Piece):
    def __init__(self, player):
        super().__init__(player)
        self.animal = "Rat"
        self.index = 0
