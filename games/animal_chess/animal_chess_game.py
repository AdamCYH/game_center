import datetime

from games.animal_chess.animal_chess_board import AnimalChessBoard
from games.animal_chess.animal_chess_piece import EmptyCard
from games.game import Game

ID_LENGTH = 5


class AnimalChessGame(Game):

    def __init__(self):
        super().__init__()
        self.max_duration = 1800  # in seconds
        self.board = None
        self.player1 = None
        self.player2 = None
        self.start_time = None
        self.started = False
        self.turn = None

    def new_game(self, player):
        self.id = self.generate_id(ID_LENGTH)
        self.player1 = player
        self.board = AnimalChessBoard()
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
        return True

    def check_win(self):
        if len(self.player1.piece_collection.pieces) == 0 and len(self.player2.piece_collection.pieces) == 0:
            self.finished = True
            return True, None
        if len(self.player1.piece_collection.pieces) == 0:
            self.finished = True
            return True, self.player2
        if len(self.player2.piece_collection.pieces) == 0:
            self.finished = True
            return True, self.player1
        return False, None

    def process_move(self, src_piece, dest_piece):
        self.board.process_piece_move(src_piece, dest_piece)

    def within_game_time_limit(self):
        if self.start_time is None or (datetime.datetime.now() - self.start_time).seconds < self.max_duration:
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
        if 0 <= x < self.board.width and 0 <= y < self.board.height:
            return True, x, y
        else:
            print("Coordinates entered is not on board")
            return False, 0, 0

    def switch_turn(self):
        if self.player1.my_turn:
            self.turn = self.player2
        else:
            self.turn = self.player1
        self.player1.my_turn = not self.player1.my_turn
        self.player2.my_turn = not self.player2.my_turn
        return self.turn

    def select_piece(self, x, y):
        piece = self.board.get_piece(x, y)
        if piece.status == 0:
            piece.flip()
            self.switch_turn()
            return False, None
        elif isinstance(piece, EmptyCard):
            return False, None
        elif piece.player != self.turn:
            return False, None
        else:
            movable_directions, movable_coordinates = self.board.get_movable_directions(piece)
            if len(movable_directions) > 0:
                return True, movable_coordinates
            else:
                return False, None

    def move_piece(self, src_coordinate, dest_coordinate):
        src_piece = self.board.get_piece(src_coordinate[0], src_coordinate[1])
        dest_piece = self.board.get_piece(dest_coordinate[0], dest_coordinate[1])
        movable_directions, movable_coordinates = self.board.get_movable_directions(src_piece)
        if dest_coordinate not in movable_coordinates:
            return
        self.process_move(src_piece, dest_piece)
        self.switch_turn()
