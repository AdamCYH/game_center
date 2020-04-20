from core.game.board import AnimalChessBoard
from core.game.player import Player


class Game:
    def __init__(self):
        self.board = None
        self.player1 = None
        self.player2 = None

    def new_game(self, player):
        pass

    def join_player(self, player):
        pass

    def start_game(self):
        pass


class AnimalChessGame(Game):
    def __init__(self):
        super().__init__()

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
        self.board.generate_board(self.player1, self.player2)


if __name__ == '__main__':
    game = AnimalChessGame()
    player1 = Player("1", "p1")
    player2 = Player("2", "p2")
    game.new_game(player1)
    game.join_player(player2)
    player1.change_status()
    player2.change_status()

    game.start_game()
    print(game.board)
