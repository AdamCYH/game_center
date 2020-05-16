from django.shortcuts import render


def home_page(request):
    return render(request, 'animal_chess/home.html')
