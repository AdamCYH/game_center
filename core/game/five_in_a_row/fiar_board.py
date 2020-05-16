from random import randint

from core.game.board import Board
from core.game.five_in_a_row.fiar_piece import EmptyPiece

PRINT_WIDTH = "{0: <3}"


class FiveInARowBoard(Board):
    def __init__(self):
        super().__init__()
        self.coordinates = [[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]]
        self.width = 15
        self.height = 15

    def init_board(self, player1, player2):
        for r in range(len(self.coordinates)):
            for c in range(len(self.coordinates[0])):
                self.coordinates[r][c] = EmptyPiece()

    def get_piece(self, x, y):
        return self.coordinates[x][y]

    def set_piece(self, piece, x, y):
        self.coordinates[x][y] = piece

    def process_piece_move(self, src_piece, dest_piece):
        pass

    def validate_position(self, x, y):
        if isinstance(self.coordinates[x][y], EmptyPiece):
            return True
        return False

    def __str__(self):
        if self.coordinates is None:
            return "No board available"
        board_string = "   "
        for x in range(self.width):
            board_string += "{0: <3}".format(x)
        board_string += "\n"
        for r in range(len(self.coordinates)):
            board_string += PRINT_WIDTH.format(r)
            board_string += '  '.join(str(v) for v in self.coordinates[r])
            board_string += "\n"
        return board_string
