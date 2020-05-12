from core.game.five_in_a_row.fiar_board import FiveInARowBoard
from core.game.player import Player

board = FiveInARowBoard()
player1 = Player("1", "Adam")
player2 = Player("2", "Yawen")
board.init_board(player1, player2)
print(board)