class PieceCollection:
    def __init__(self):
        self.pieces = None


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
        if self.status is 0:
            self.status = 1

    def move(self, dest_x, dest_y):
        pass

    def set_player(self, player):
        self.player = player

    def get_status(self):
        return self.status

    def __str__(self):
        if self.status == 0:
            return "#####"
        return "{}:{}".format(self.player, self.animal)

    def __repr__(self):
        return "{}:{}".format(self.player, self.animal)


class AnimalChessPiece(Piece):
    directions = {"up": [-1, 0], "down": [1, 0], "left": [0, -1], "right": [0, 1]}

    def __init__(self, player):
        super().__init__(player)

    def move(self, dest_x, dest_y):
        self.x = dest_x
        self.y = dest_y


class EmptyCard(AnimalChessPiece):
    def __init__(self, player):
        super().__init__(player)
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
