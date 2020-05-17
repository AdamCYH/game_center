from django.shortcuts import render, redirect
from django.views import View

CODE_LENGTH = 5


def home_page(request):
    return render(request, 'core/home.html')


class UserView(View):
    def get(self, request):
        return render(request, 'core/login.html')

    def post(self, request):
        if request.POST:
            name = request.POST.get("name")
            request.session['name'] = name
        if request.POST.get("new_game") == "True":
            return redirect(resolve_path(request, "game"))
        return redirect(request.GET["next"])


def join_page(request):
    if 'name' in request.session:
        return render(request, 'core/join.html')
    else:
        return redirect(resolve_path(request, "user?next=") + resolve_path(request, "join_game"))


def resolve_path(request, path):
    game = request.get_full_path().split("/")[1]
    return "/{}/{}".format(game, path)


class MessageTemplates:
    GAME_NOT_FOUND = "No game found"
    GAME_FULL = "The game you are trying to enter is full is full"
