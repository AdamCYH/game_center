import json

from channels.generic.websocket import WebsocketConsumer

from core.views import games


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        data = json.loads(text_data)
        action = data['action']
        player = data['player']
        board = []

        if action == 'ready':
            game = games[data['gameID']]

            if player == '1':
                game.player1.ready = True
            else:
                game.player2.ready = True

            if game.player1 and game.player2 and game.player1.ready and game.player2.ready:
                action = 'start game'
                board = game.board.coordinates
        if action == 'move':
            game = games[data['gameID']]

        self.send(text_data=json.dumps({
            'action': action,
            'board': board,
            'message': player + ":" + action
        }))
