"""animal_chess URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from core import views
from core.views import AnimalChessGameView, UserView

urlpatterns = [
    path('', views.home_page, name='animal-chess-home'),
    path('game/', AnimalChessGameView.as_view(), name='animal-game'),
    path('user/', UserView.as_view(), name='animal-user'),
    path('join_game', views.join_page, name='animal-join-page'),
    path('ready', views.ready, name='animal-ready'),
]