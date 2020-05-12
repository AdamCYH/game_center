import datetime

from core.game.five_in_a_row.fiar_board import FiveInARowBoard
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
        return True

    def check_win(self):
        return False, None

    def within_game_time_limit(self):
        if (datetime.datetime.now() - self.start_time).seconds < self.max_duration:
            return True
        else:
            return False
