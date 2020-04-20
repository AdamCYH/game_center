import random

from core.game.card import AnimalChessPieceCollection, EmptyCard, AnimalChessPiece

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


class AnimalChessBoard(Board):
    def __init__(self):
        super().__init__()
        self.coordinates = [[None, None, None, None],
                            [None, None, None, None],
                            [None, None, None, None],
                            [None, None, None, None]]
        self.width = 4
        self.height = 4

    def init_board(self, player1, player2):
        player1.piece_collection = AnimalChessPieceCollection(player1).pieces
        player2.piece_collection = AnimalChessPieceCollection(player2).pieces

        cards = []
        cards.extend(player1.piece_collection)
        cards.extend(player2.piece_collection)
        random.shuffle(cards)

        for r in range(len(self.coordinates)):
            for c in range(len(self.coordinates[0])):
                card_idx = r * self.width + c
                cards[card_idx].x = r
                cards[card_idx].y = c
                self.coordinates[r][c] = cards[card_idx]

    def get_piece(self, x, y):
        return self.coordinates[x][y]

    def set_piece(self, piece, x, y):
        self.coordinates[x][y] = piece

    def process_piece_move(self, src_piece, dest_piece):
        # TODO If dest_piece is empty, set_piece
        # If dest_piece is not empty, compare and replace the piece

        self.set_piece(src_piece, dest_piece.x, dest_piece.y)
        self.set_piece(EmptyCard(None), src_piece.x, src_piece.y)
        src_piece.move(dest_piece.x, dest_piece.y)

    def is_movable(self, src_piece, dest_x, dest_y):
        """
        Validate beyond boundary and within boundary positions
        :param src_piece:
        :param dest_x:
        :param dest_y:
        :return:
        """
        # TODO can only move if the destination position is empty or opponent's card
        if dest_x < 0 or dest_x >= self.width or dest_y < 0 or dest_y >= self.height:
            return False
        else:
            return True

    def get_movable_directions(self, src_piece):

        movable_directions = []
        for direction in AnimalChessPiece.directions.keys():
            dest_x = src_piece.x + AnimalChessPiece.directions[direction][0]
            dest_y = src_piece.y + AnimalChessPiece.directions[direction][1]
            if self.is_movable(src_piece, dest_x, dest_y):
                movable_directions.append(direction)
        return movable_directions
