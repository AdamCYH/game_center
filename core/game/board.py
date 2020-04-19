class Board:
    def __init__(self):
        self.board = [[None, None, None, None],
                      [None, None, None, None],
                      [None, None, None, None],
                      [None, None, None, None]]
        self.player1 = None
        self.player2 = None

    def new_game(self, player):
        self.player1 = player
        self.board = self.generate_board()
        return

    def join_game(self, player):
        self.player2 = player

    def flip(self):
        return

    def move(self):
        return

    @staticmethod
    def generate_board():
        return []
