import datetime

from core.game.animal_chess.animal_chess_game import AnimalChessGame
from core.game.animal_chess.animal_chess_piece import AnimalChessPiece
from core.game.animal_chess.animal_chess_player import AnimalChessPlayer

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
        print("Time remaining: {}".format(game.max_duration - (datetime.datetime.now() - game.start_time).seconds))
        print("### {}'s turn ###".format(player_turn.name))
        coords = input("Click coordinate (x y), enter x [space] y\n")
        parse_successful, x, y = game.parse_input_to_coords(coords)
        if not parse_successful:
            continue

        piece = game.board.get_piece(x, y)
        if piece.status == 0:
            piece.flip()
        else:
            movable_directions, coordinate = game.board.get_movable_directions(piece)
            if len(movable_directions) != 0:
                direction = input("Where would you like to move? Enter {}\n".format(movable_directions))
                while direction not in movable_directions:
                    direction = input(
                        "Invalid move. Where would you like to move? Enter {}\n".format(movable_directions))
                dest_x = piece.x + AnimalChessPiece.directions[direction][0]
                dest_y = piece.y + AnimalChessPiece.directions[direction][1]
                dest_piece = game.board.get_piece(dest_x, dest_y)
                game.process_move(piece, dest_piece)
            else:
                player_turn = game.switch_turn()

        player_turn = game.switch_turn()

    finish, winner = game.check_win()
    if winner is None:
        print("TIE!!!")
    else:
        print(winner.name + " is the winner, Congratulations!!!")
