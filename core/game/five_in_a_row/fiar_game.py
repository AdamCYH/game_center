import copy
import datetime

from core.game.five_in_a_row.fiar_board import FiveInARowBoard
from core.game.five_in_a_row.fiar_piece import BlackPiece, WhitePiece
from core.game.game import Game

ID_LENGTH = 5


class FiveInARowGame(Game):
    def __init__(self):
        super().__init__()
        self.max_duration = 3600  # in seconds
        self.board = None
        self.player1 = None
        self.player2 = None
        self.start_time = None
        self.started = False
        self.turn = None

    def new_game(self, player):
        self.id = self.generate_id(ID_LENGTH)
        self.player1 = player
        self.board = FiveInARowBoard()
        self.player1.my_turn = True
        self.turn = self.player1

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
        self.started = True
        # TODO randomize player order
        self.player1.piece_collection = BlackPiece(self.player1)
        self.player2.piece_collection = WhitePiece(self.player2)

        return True

    def check_win(self):
        return False, None

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

    def place_piece(self, x, y):
        if self.board.validate_position(x, y):
            self.board.set_piece(copy.copy(self.turn.piece_collection), x, y)
            self.switch_turn()
            return True, x, y
        else:
            return False, x, y

    def switch_turn(self):
        if self.player1.my_turn:
            self.turn = self.player2
        else:
            self.turn = self.player1
        self.player1.my_turn = not self.player1.my_turn
        self.player2.my_turn = not self.player2.my_turn
        return self.turn
