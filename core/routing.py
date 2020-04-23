from django.urls import re_path

from core import consumers

websocket_urlpatterns = [
    re_path(r'ws/animal-chess-game/(?P<game_id>\w+)/$', consumers.ChatConsumer),
]
