from django.shortcuts import render, redirect
from django.views import View

from core.game.animal_chess.animal_chess_game import AnimalChessGame
from core.game.animal_chess.animal_chess_player import AnimalChessPlayer

games = {}
CODE_LENGTH = 5


def home_page(request):
    return render(request, 'animal_chess/home.html')


class AnimalChessGameView(View):
    # get request, return the template
    def get(self, request):
        if 'name' in request.session:
            # if player has a game in progress
            if 'code' in request.session:
                code = request.session['code']
                if code in games:
                    game = games[code]
                    context = {"code": game.id,
                               "game_in_progress": True}
                    return render(request, 'animal_chess/home.html', context)
            return redirect("/animal-chess/game/new")

        # Name is not set, redirect to login page.
        else:
            return redirect('/animal-chess/user?next=game/new')

    def post(self, request):
        clean_up_games()
        if 'name' in request.session:
            code = request.POST.get("code").upper()
            name = request.session['name']
            if code not in games:
                context = {"msg": MessageTemplates.GAME_NOT_FOUND}
                return render(request, 'animal_chess/home.html', context)
            else:
                game = games[code]
                if game.player2 is not None:
                    context = {"msg": MessageTemplates.GAME_FULL}
                    return render(request, 'animal_chess/home.html', context)
                else:
                    game.player2 = AnimalChessPlayer("2", name)
                    player_id = game.player2.user_id
                    context = {"game": game,
                               "player_id": player_id}
                    # return render(request, 'animal_chess/game.html', context)
                    return redirect('/animal-chess/game/' + game.id)
        else:
            return render(request, 'animal_chess/login.html')


def new_game(request):
    name = request.session['name']

    game = start_new_game(name)
    context = {"game": game,
               "player_id": game.player1.user_id}
    request.session['code'] = game.id
    # return render(request, 'animal_chess/game.html', context)
    return redirect('/animal-chess/game/' + game.id)


def join_page(request):
    if 'name' in request.session:
        return render(request, 'animal_chess/join.html')
    else:
        return render(request, 'animal_chess/login.html')


def access_game(request, game_id):
    if 'name' in request.session:
        if game_id in games:
            game = games[game_id]
            context = {"game": game}
            return render(request, 'animal_chess/game.html', context)
        else:
            context = {"msg": MessageTemplates.GAME_NOT_FOUND}
            return render(request, 'animal_chess/home.html', context)
    else:
        return redirect("/animal-chess/user?next=/animal-chess/game/" + game_id)


class UserView(View):
    def get(self, request):
        return render(request, 'animal_chess/login.html')

    def post(self, request):
        if request.POST:
            name = request.POST.get("name")
            request.session['name'] = name
        if request.POST.get("new_game") == "True":
            return redirect("/animal-chess/game")
        return redirect("/animal-chess/" + request.GET["next"])


def ready(request):
    pass


class MessageTemplates:
    GAME_NOT_FOUND = "No game found"
    GAME_FULL = "The game you are trying to enter is full is full"


def start_new_game(name):
    game = AnimalChessGame()
    player = AnimalChessPlayer("1", name)
    game.new_game(player)
    code = game.id
    games[code] = game
    return game


def clean_up_games():
    for g in list(games):
        if games[g].finished:
            del games[g]
