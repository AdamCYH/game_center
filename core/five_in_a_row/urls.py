from django.urls import path

from core.five_in_a_row import views
from core.five_in_a_row.views import FiveInARowView
from core.views import UserView, join_page

urlpatterns = [
    path('game/', FiveInARowView.as_view(), name='fiar-game'),
    path('game/<str:game_id>', views.access_game, name='fiar-access-game'),
    path('user/', UserView.as_view(), name='fiar-user'),
    path('join_game', join_page, name='fiar-join-page'),
]
