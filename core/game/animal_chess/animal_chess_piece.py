from core.game.piece import PieceCollection, Piece
from core.game.player import Player


class AnimalChessPieceCollection(PieceCollection):
    collection_size = 8

    def __init__(self, player):
        super().__init__()
        self.pieces = [ElephantCard(player),
                       LionCard(player),
                       TigerCard(player),
                       LeopardCard(player),
                       WolfCard(player),
                       DogCard(player),
                       CatCard(player),
                       RatCard(player)]

    def remove_piece_on_hand(self, card):
        self.pieces.remove(card)


class AnimalChessPiece(Piece):
    directions = {"up": [-1, 0], "down": [1, 0], "left": [0, -1], "right": [0, 1]}

    def __init__(self, player):
        super().__init__(player)

    def move(self, dest_x, dest_y):
        self.x = dest_x
        self.y = dest_y


class EmptyCard(AnimalChessPiece):
    def __init__(self):
        default_player = Player("", "")
        super().__init__(default_player)
        self.animal = ""
        self.index = -1
        self.status = 1


class ElephantCard(AnimalChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self.animal = "Elephant"
        self.index = 7


class LionCard(AnimalChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self.animal = "Lion"
        self.index = 6


class TigerCard(AnimalChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self.animal = "Tiger"
        self.index = 5


class LeopardCard(AnimalChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self.animal = "Leopard"
        self.index = 4


class WolfCard(AnimalChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self.animal = "Wolf"
        self.index = 3


class DogCard(AnimalChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self.animal = "Dog"
        self.index = 2


class CatCard(AnimalChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self.animal = "Cat"
        self.index = 1


class RatCard(AnimalChessPiece):
    def __init__(self, player):
        super().__init__(player)
        self.animal = "Rat"
        self.index = 0
