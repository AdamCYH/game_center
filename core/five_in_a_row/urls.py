
from django.urls import path

from core.animal_chess import views
from core.animal_chess.views import AnimalChessGameView
from core.views import UserView, join_page

urlpatterns = [
    path('game/', AnimalChessGameView.as_view(), name='animal-game'),
    path('game/<str:game_id>', views.access_game, name='animal-access-game'),
    path('user/', UserView.as_view(), name='animal-user'),
    path('join_game', join_page, name='animal-join-page'),
]
