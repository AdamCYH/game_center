from games.piece import Piece
from games.player import Player


class FiveInARowPiece(Piece):
    def __init__(self, player):
        super().__init__(player)


class EmptyPiece(FiveInARowPiece):
    def __init__(self):
        default_player = Player("", "")
        super().__init__(default_player)
        self.name = ""
        self.index = 0

    def __str__(self):
        return "+"

    def __repr__(self):
        return "+"


class BlackPiece(FiveInARowPiece):
    def __init__(self, player):
        super().__init__(player)
        self.name = "Black"
        self.index = 1

    def __str__(self):
        return "o"

    def __repr__(self):
        return "o"


class WhitePiece(FiveInARowPiece):
    def __init__(self, player):
        super().__init__(player)
        self.name = "White"
        self.index = 2

    def __str__(self):
        return "x"

    def __repr__(self):
        return "x"
