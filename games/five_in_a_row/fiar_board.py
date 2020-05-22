from games.board import Board
from games.five_in_a_row.fiar_piece import EmptyPiece

PRINT_WIDTH = "{0: <3}"


class FiveInARowBoard(Board):
    def __init__(self):
        super().__init__()
        self.coordinates = ([None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
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
                            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None])
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

    # Check if the piece can be placed here.
    def is_available_space(self, x, y):
        if not self.is_in_boundary(x, y):
            return False
        if isinstance(self.coordinates[x][y], EmptyPiece):
            return True
        return False

    def is_in_boundary(self, x, y):
        if x >= self.height or x < 0 or y >= self.width or y < 0:
            return False
        return True

    def serialize(self):
        board_json = []
        for row in self.coordinates:
            row_json = []
            for col in row:
                row_json.append({"piece": col.name,
                                 "player": col.player.user_id})
            board_json.append(row_json)
        return board_json

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
