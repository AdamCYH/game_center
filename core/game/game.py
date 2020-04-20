import random

from core.game.board import AnimalChessBoard
from core.game.card import CardCollection
from core.game.player import Player


class Game:
    def __init__(self):
        self.board = None
        self.player1 = None
        self.player2 = None

    def new_game(self, player):
        self.player1 = player

        return

    def join_game(self, player):
        self.player2 = player

    def start_game(self, ):
        if self.player1 is None or self.player2 is None:
            return "Waiting for player to join."
        if not self.player1.ready or not self.player2.ready:
            return "Please click ready before starting."
        self.board = AnimalChessBoard()
        self.generate_board()

    def flip(self):
        return

    def move(self):
        return

    def generate_board(self):
        player1_cards = CardCollection(self.player1).cards
        player2_cards = CardCollection(self.player2).cards

        cards = []
        cards.extend(player1_cards)
        cards.extend(player2_cards)
        random.shuffle(cards)

        for r in range(len(self.board.coordinates)):
            for c in range(len(self.board.coordinates[0])):
                self.board.coordinates[r][c] = cards[r * self.board.width + c]


if __name__ == '__main__':
    game = Game()
    player1 = Player()
    player1.__set_name__("1", "p1")
    player2 = Player()
    player2.__set_name__("1", "p2")
    game.new_game(player1)
    game.join_game(player2)
    player1.change_status()
    player2.change_status()

    game.start_game()
    print(game.board)
