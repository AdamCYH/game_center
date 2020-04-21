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
        player1.piece_collection = AnimalChessPieceCollection(player1)
        player2.piece_collection = AnimalChessPieceCollection(player2)

        cards = []
        cards.extend(player1.piece_collection.pieces)
        cards.extend(player2.piece_collection.pieces)
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
        if not isinstance(dest_piece, EmptyCard):
            fight_result = self.compare_rank(src_piece, dest_piece)
            if fight_result == 1:
                self.destroy_dest(src_piece, dest_piece)
            elif fight_result == -1:
                self.src_destroyed(src_piece)
            else:
                self.destroy_both(src_piece, dest_piece)

        else:
            self.switch_position(src_piece, dest_piece)

    @staticmethod
    def compare_rank(src_piece, dest_piece):
        # 1 src_piece > dest_piece
        # 0 src_piece = dest_piece
        # -1 src_piece < dest_piece

        if AnimalChessPieceCollection.collection_size - 1 > src_piece.index - dest_piece.index > 0 \
                or src_piece.index - dest_piece.index == (1 - AnimalChessPieceCollection.collection_size):
            return 1
        elif src_piece.index < dest_piece.index \
                or src_piece.index - dest_piece.index == AnimalChessPieceCollection.collection_size - 1:
            return -1
        else:
            return 0

    def switch_position(self, src_piece, dest_piece):
        tmp_src_x = src_piece.x
        tmp_src_y = src_piece.y
        tmp_dest_x = dest_piece.x
        tmp_dest_y = dest_piece.y

        src_piece.move(tmp_dest_x, tmp_dest_y)
        dest_piece.move(tmp_src_x, tmp_src_y)

        self.set_piece(src_piece, tmp_dest_x, tmp_dest_y)
        self.set_piece(dest_piece, tmp_src_x, tmp_src_y)

    def replace_piece(self, new_piece, old_piece):
        new_piece.x = old_piece.x
        new_piece.y = old_piece.y
        self.set_piece(new_piece, old_piece.x, old_piece.y)

    def destroy_dest(self, src_piece, dest_piece):
        self.switch_position(src_piece, dest_piece)
        self.replace_piece(EmptyCard(), dest_piece)
        dest_piece.player.piece_collection.remove_piece_on_hand(dest_piece)

    def src_destroyed(self, src_piece):
        self.replace_piece(EmptyCard(), src_piece)
        src_piece.player.piece_collection.remove_piece_on_hand(src_piece)

    def destroy_both(self, src_piece, dest_piece):
        self.replace_piece(EmptyCard(), src_piece)
        self.replace_piece(EmptyCard(), dest_piece)
        src_piece.player.piece_collection.remove_piece_on_hand(src_piece)
        dest_piece.player.piece_collection.remove_piece_on_hand(dest_piece)

    def is_movable(self, src_piece, dest_x, dest_y):
        """
        Validate beyond boundary and within boundary positions
        :param src_piece:
        :param dest_x:
        :param dest_y:
        :return:
        """
        if dest_x < 0 or dest_x >= self.width or dest_y < 0 or dest_y >= self.height:
            return False
        elif self.coordinates[dest_x][dest_y].status == 0:
            return False
        elif self.coordinates[dest_x][dest_y].player == src_piece.player:
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
