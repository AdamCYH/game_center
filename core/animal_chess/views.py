from django.shortcuts import render, redirect
from django.views import View

from games.animal_chess.animal_chess_game import AnimalChessGame
from games.animal_chess.animal_chess_player import AnimalChessPlayer

games = {}
CODE_LENGTH = 5


class AnimalChessGameView(View):
    # get request, return the template
    def get(self, request):
        print(request.get_full_path())
        if 'name' in request.session:
            # if player has a game in progress
            if 'code' in request.session:
                code = request.session['code']
                if code in games:
                    game = games[code]
                    if not game.finished:
                        context = {"code": game.id,
                                   "game_in_progress": True}
                        return render(request, 'core/home.html', context)
            return redirect("/animal-chess/game/new")

        # Name is not set, redirect to login page.
        else:
            return redirect('/animal-chess/user?next=/animal-chess/game/new')

    def post(self, request):
        clean_up_games()
        if 'name' in request.session:
            code = request.POST.get("code").upper()
            name = request.session['name']
            if code not in games:
                context = {"msg": MessageTemplates.GAME_NOT_FOUND}
                return render(request, 'core/home.html', context)
            else:
                return redirect('/animal-chess/game/' + code)
        else:
            return render(request, 'core/login.html')


def join_page(request):
    if 'name' in request.session:
        return render(request, 'core/join.html')
    else:
        return redirect('/animal-chess/user?next=/animal-chess/join_game')


def access_game(request, game_id):
    if 'name' in request.session:
        name = request.session['name']
        if game_id == 'new':
            game = start_new_game(name, request.session.session_key)
            request.session['code'] = game.id
            return redirect('/animal-chess/game/' + game.id)
        if game_id in games:
            user_id = request.session.session_key
            game = games[game_id]

            # if player1, can only be reconnection
            if (game.player1 and game.player1.user_id == user_id) or (game.player2 and game.player2.user_id == user_id):
                context = {"game": game,
                           "player_id": user_id,
                           "status": "reconnect"}
                if not game.started:
                    context['status'] = 'join'
                return render(request, 'animal_chess/game.html', context)
            # if user is not player1 nor player2, game is full
            elif (game.player1 and game.player1.user_id != user_id) and (
                    game.player2 and game.player2.user_id != user_id):
                context = {"msg": MessageTemplates.GAME_FULL}
                return render(request, 'core/home.html', context)
            # game has space
            else:
                request.session['code'] = game.id
                context = {"game": game,
                           "player_id": user_id}
                game.player2 = AnimalChessPlayer(request.session.session_key, name)
                return render(request, 'animal_chess/game.html', context)
        else:
            context = {"msg": MessageTemplates.GAME_NOT_FOUND}
            return render(request, 'core/home.html', context)
    else:
        return redirect("/animal-chess/user?next=/animal-chess/game/" + game_id)


class UserView(View):
    def get(self, request):
        return render(request, 'core/login.html')

    def post(self, request):
        if request.POST:
            name = request.POST.get("name")
            request.session['name'] = name
        if request.POST.get("new_game") == "True":
            return redirect("/animal-chess/game")
        return redirect(request.GET["next"])


class MessageTemplates:
    GAME_NOT_FOUND = "No game found"
    GAME_FULL = "The game you are trying to enter is full is full"


def start_new_game(name, user_id):
    game = AnimalChessGame()
    player = AnimalChessPlayer(user_id, name)
    game.new_game(player)
    code = game.id
    games[code] = game
    return game


def clean_up_games():
    for g in list(games):
        if games[g].finished:
            del games[g]
