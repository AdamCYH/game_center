from django.shortcuts import render


# Create your views here.


def home_page(request):
    return render(request, 'animal_chess/index.html')


def start_game(request):
    context = {"code": "12345"}
    return render(request, 'animal_chess/game.html', context)
