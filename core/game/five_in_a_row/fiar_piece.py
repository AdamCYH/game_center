from core.game.piece import Piece
from core.game.player import Player


class FiveInARowPiece(Piece):
    def __init__(self, player):
        super().__init__(player)

    def __str__(self):
        if isinstance(self, EmptyPiece):
            return "+"
        if isinstance(self, BlackPiece):
            return "o"
        if isinstance(self, WhitePiece):
            return "x"

    def __repr__(self):
        if isinstance(self, EmptyPiece):
            return "+"
        if isinstance(self, BlackPiece):
            return "o"
        if isinstance(self, WhitePiece):
            return "x"


class EmptyPiece(FiveInARowPiece):
    def __init__(self):
        default_player = Player("", "")
        super().__init__(default_player)
        self.name = ""
        self.index = 0


class BlackPiece(FiveInARowPiece):
    def __init__(self, player):
        super().__init__(player)
        self.name = "Black"
        self.index = 1


class WhitePiece(FiveInARowPiece):
    def __init__(self, player):
        super().__init__(player)
        self.name = "White"
        self.index = 2
