from django.urls import re_path

from core.animal_chess import consumers as animal_chess_consumers
from core.five_in_a_row import consumers as five_in_a_row_consumers

websocket_urlpatterns = [
    re_path(r'ws/animal-chess-game/(?P<game_id>\w+)/$', animal_chess_consumers.ChatConsumer),
    re_path(r'ws/five-in-a-row-game/(?P<game_id>\w+)/$', five_in_a_row_consumers.ChatConsumer),
]
