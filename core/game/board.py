import random

from core.game.card import CardCollection


class Board:
    def __init__(self):
        self.coordinates = None
        self.width = 0
        self.height = 0

    def __str__(self):
        if self.coordinates is None:
            return "No board available"
        board_string = ""
        for r in range(len(self.coordinates)):
            for c in range(len(self.coordinates[0])):
                board_string += "{0: <15}".format(str(self.coordinates[r][c]))
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

    def generate_board(self, player1, player2):
        player1_cards = CardCollection(player1).cards
        player2_cards = CardCollection(player2).cards

        cards = []
        cards.extend(player1_cards)
        cards.extend(player2_cards)
        random.shuffle(cards)

        for r in range(len(self.coordinates)):
            for c in range(len(self.coordinates[0])):
                self.coordinates[r][c] = cards[r * self.width + c]
