from django.shortcuts import render, redirect
from django.views import View

from core.game.animal_chess.animal_chess_game import AnimalChessGame
from core.game.animal_chess.animal_chess_player import AnimalChessPlayer

games = {}
CODE_LENGTH = 5


def home_page(request):
    return render(request, 'animal_chess/home.html')


def join_page(request):
    return render(request, 'animal_chess/join.html')


class AnimalChessGameView(View):
    # get request, return the template
    def get(self, request):
        if request.GET.get("reconnect"):
            if 'code' in request.session and 'name' in request.session:
                code = request.session['code']
                name = request.session['name']
                if code in games:
                    game = games[code]
                    context = {"game", game}
                    return render(request, 'animal_chess/game.html', context)
            context = {'msg': MessageTemplates.GAME_NOT_FOUND}
            return render(request, 'animal_chess/home.html', context)

        if 'name' in request.session:
            name = request.session['name']

            game = start_new_game(name)
            context = {"game": game,
                       "player_id": game.player1.user_id}
            return render(request, 'animal_chess/game.html', context)
        else:
            return render(request, 'animal_chess/login.html')

    def post(self, request):
        if 'name' in request.session:
            code = request.POST.get("code")
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
                    return render(request, 'animal_chess/game.html', context)
        else:
            return render(request, 'animal_chess/login.html')


class UserView(View):
    def post(self, request):
        name = request.POST.get("name")
        request.session['name'] = name
        return redirect('/animal-chess/game', request)


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
