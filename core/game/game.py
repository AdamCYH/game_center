import random
import string

DEFAULT_LENGTH = 5


class Game:
    def __init__(self):
        self.id = None
        self.board = None
        self.player1 = None
        self.player2 = None
        self.start_time = None
        self.turn = None
        self.finished = False

    def new_game(self, player):
        pass

    def join_player(self, player):
        pass

    def start_game(self):
        pass

    def check_win(self, *args, **kwargs):
        pass

    @staticmethod
    def generate_id(length=DEFAULT_LENGTH):
        return ''.join(random.choices(string.ascii_uppercase +
                                      string.digits, k=length))
