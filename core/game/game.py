import datetime

from core.game.board import AnimalChessBoard
from core.game.card import AnimalChessPiece
from core.game.player import AnimalChessPlayer


class Game:
    def __init__(self):
        self.board = None
        self.player1 = None
        self.player2 = None
        self.start_time = None

    def new_game(self, player):
        pass

    def join_player(self, player):
        pass

    def start_game(self):
        pass

    def check_win(self):
        pass


class AnimalChessGame(Game):

    def __init__(self):
        super().__init__()
        self.max_duration = 1800  # in seconds

    def new_game(self, player):
        self.player1 = player

        return

    def join_player(self, player):
        self.player2 = player

    def start_game(self):
        if self.player1 is None or self.player2 is None:
            return "Waiting for player to join."
        if not self.player1.ready or not self.player2.ready:
            return "Please click ready before starting."
        self.board = AnimalChessBoard()
        self.board.init_board(self.player1, self.player2)
        self.start_time = datetime.datetime.now()
        self.player1.my_turn = True
        return True

    def check_win(self):
        if len(self.player1.piece_collection.pieces) == 0 and len(self.player2.piece_collection) == 0:
            return True, None
        if len(self.player1.piece_collection.pieces) == 0:
            return True, player2
        if len(self.player2.piece_collection.pieces) == 0:
            return True, player1
        return False, None

    def process_move(self, direction, src_piece):
        dest_x = src_piece.x + AnimalChessPiece.directions[direction][0]
        dest_y = src_piece.y + AnimalChessPiece.directions[direction][1]
        dest_piece = self.board.get_piece(dest_x, dest_y)
        self.board.process_piece_move(src_piece, dest_piece)

    def within_game_time_limit(self):
        if (datetime.datetime.now() - self.start_time).seconds < game.max_duration:
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
            turn = player2
        else:
            turn = player1
        self.player1.my_turn = not self.player1.my_turn
        self.player2.my_turn = not self.player2.my_turn
        return turn


if __name__ == '__main__':
    game = AnimalChessGame()
    player1 = AnimalChessPlayer("1", "p1")
    player2 = AnimalChessPlayer("2", "p2")
    game.new_game(player1)
    game.join_player(player2)
    player1.change_status()
    player2.change_status()

    game.start_game()

    player_turn = player1

    while not game.check_win()[0] and game.within_game_time_limit():
        print()
        print(game.board)
        print("Time remaining: {}".format(datetime.datetime.now() - game.start_time))
        print("### {}'s turn ###".format(player_turn.name))
        coords = input("Click coordinate (x y), enter x [space] y\n")
        parse_successful, x, y = game.parse_input_to_coords(coords)
        if not parse_successful:
            continue

        piece = game.board.get_piece(x, y)
        if piece.status == 0:
            piece.flip()
        else:
            movable_directions = game.board.get_movable_directions(piece)
            if len(movable_directions) != 0:
                direction = input("Where would you like to move? Enter {}\n".format(movable_directions))
                while direction not in movable_directions:
                    direction = input(
                        "Invalid move. Where would you like to move? Enter {}\n".format(movable_directions))
                game.process_move(direction, piece)
            else:
                player_turn = game.switch_turn()

        player_turn = game.switch_turn()
