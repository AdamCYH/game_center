PRINT_WIDTH = "{0: <15}"


class Board:
    def __init__(self):
        self.coordinates = None
        self.width = 0
        self.height = 0

    def init_board(self, player1, player2):
        pass

    def get_piece(self, x, y):
        pass

    def process_piece_move(self, src_piece, dest_piece):
        pass

    def validate_position(self, x, y):
        pass

    def __str__(self):
        if self.coordinates is None:
            return "No board available"
        board_string = "  "
        for x in range(self.width):
            board_string += PRINT_WIDTH.format(x)
        board_string += "\n"
        for r in range(len(self.coordinates)):
            board_string += "{} ".format(r)
            for c in range(len(self.coordinates[0])):
                board_string += PRINT_WIDTH.format(str(self.coordinates[r][c]))
            board_string += "\n"
        return board_string

    def serialize(self):
        board_json = []
        for row in self.coordinates:
            row_json = []
            for col in row:
                if col.status == 1:
                    row_json.append({"name": col.name})
                else:
                    row_json.append({"name": "hidden"})
            board_json.append(row_json)
        return board_json
