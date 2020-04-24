import datetime
import random
import string

from core.game.animal_chess.animal_chess_board import AnimalChessBoard
from core.game.animal_chess.animal_chess_piece import AnimalChessPiece
from core.game.game import Game

ID_LENGTH = 5


class AnimalChessGame(Game):

    def __init__(self):
        super().__init__()
        self.max_duration = 1800  # in seconds
        self.board = None
        self.player1 = None
        self.player2 = None
        self.start_time = None

    def new_game(self, player):
        self.id = self.generate_id(ID_LENGTH)
        self.player1 = player
        self.board = AnimalChessBoard()
        return

    def join_player(self, player):
        self.player2 = player

    def start_game(self):
        if self.player1 is None or self.player2 is None:
            return "Waiting for player to join."
        if not self.player1.ready or not self.player2.ready:
            return "Please click ready before starting."
        self.board.init_board(self.player1, self.player2)
        self.start_time = datetime.datetime.now()
        self.player1.my_turn = True
        return True

    def check_win(self):
        if len(self.player1.piece_collection.pieces) == 0 and len(self.player2.piece_collection.pieces) == 0:
            return True, None
        if len(self.player1.piece_collection.pieces) == 0:
            return True, self.player2
        if len(self.player2.piece_collection.pieces) == 0:
            return True, self.player1
        return False, None

    def process_move(self, direction, src_piece):
        dest_x = src_piece.x + AnimalChessPiece.directions[direction][0]
        dest_y = src_piece.y + AnimalChessPiece.directions[direction][1]
        dest_piece = self.board.get_piece(dest_x, dest_y)
        self.board.process_piece_move(src_piece, dest_piece)

    def within_game_time_limit(self):
        if (datetime.datetime.now() - self.start_time).seconds < self.max_duration:
            return True
        else:
            return False

    def parse_input_to_coords(self, user_inputs):
        coordinate = user_inputs.split(" ")
        if len(coordinate) != 2:
            print("Please enter TWO numbers only")
            return False, 0, 0
        try:
            x = int(coordinate[0])
            y = int(coordinate[1])
            return self.validate_coordinates_value(x, y)
        except TypeError or ValueError:
            print("Please enter valid number")
            return False, 0, 0

    def validate_coordinates_value(self, x, y):
        if 0 <= x <= self.board.width and 0 <= y <= self.board.height:
            return True, x, y
        else:
            print("Coordinates entered is not on board")
            return False, 0, 0

    def switch_turn(self):
        if self.player1.my_turn:
            turn = self.player2
        else:
            turn = self.player1
        self.player1.my_turn = not self.player1.my_turn
        self.player2.my_turn = not self.player2.my_turn
        return turn

    def select_piece(self, x, y):
        piece = self.board.get_piece(x, y)
        if piece.status == 0:
            piece.flip()
        # else:
        #     movable_directions = self.board.get_movable_directions(piece)
        #     if len(movable_directions) != 0:
        #         direction = input("Where would you like to move? Enter {}\n".format(movable_directions))
        #         while direction not in movable_directions:
        #             direction = input(
        #                 "Invalid move. Where would you like to move? Enter {}\n".format(movable_directions))
        #         game.process_move(direction, piece)
        #     else:
        #         player_turn = game.switch_turn()

    @staticmethod
    def generate_id(length):
        return ''.join(random.choices(string.ascii_uppercase +
                                      string.digits, k=length))
