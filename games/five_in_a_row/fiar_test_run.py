import datetime

from games.five_in_a_row.fiar_game import FiveInARowGame
from games.five_in_a_row.fiar_player import FiveInARowPlayer

if __name__ == '__main__':
    game = FiveInARowGame()
    player1 = FiveInARowPlayer("1", "p1")
    player2 = FiveInARowPlayer("2", "p2")
    game.new_game(player1)
    game.join_player(player2)
    player1.change_status()
    player2.change_status()

    game.start_game()

    finish = False
    winner = None

    while not finish and game.within_game_time_limit():
        print()
        print(game.board)
        print("Time remaining: {}".format(game.max_duration - (datetime.datetime.now() - game.start_time).seconds))
        print("### {}'s turn ###".format(game.turn))
        coords = input("Click coordinate (x y), enter x [space] y\n")
        parse_successful, x, y = game.parse_input_to_coords(coords)
        if not parse_successful:
            continue

        place_successful, x, y = game.place_piece(x, y)
        finish, winner = game.check_win((x, y))

    if winner is None:
        print("TIE!!!")
    else:
        print(winner.name + " is the winner, Congratulations!!!")


def generate_board_html():
    string = ""
    for row in range(15):
        string += "<tr>"
        for col in range(15):
            string += "<td id=\"{}-{}\" class=\"grid\"></td>".format(row, col)
        string += "</tr>"

    print(string)
