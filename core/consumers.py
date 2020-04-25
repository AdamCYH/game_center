import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from core.views import games


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.game_id,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.game_id,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        print(text_data)
        data = json.loads(text_data)
        action = data['action']
        player_name = data['player_name']
        player_id = data['player_id']
        board = []
        message = {}
        movable = False
        if action == 'chat':
            message.update({
                'message': player_name + ": " + data['message']
            })
        else:
            game = games[data['gameID']]
            if action == 'ready':
                if player_id == game.player1.user_id:
                    game.player1.change_status()
                else:
                    game.player2.change_status()

                if game.player1 and game.player2 and game.player1.ready and game.player2.ready:
                    action = 'start game'
                    game.start_game()
            elif action == 'join':
                message.update({"player_id": player_id,
                                "player_name": player_name})
            elif action == 'select':
                if player_id == game.turn.user_id:
                    x, y = data['coordinate'].split("-")
                    movable, movable_coordinates = game.select_piece(int(x), int(y))
                    if movable:
                        message.update({'movable_coordinates': movable_coordinates})
            elif action == 'move':
                if player_id == game.turn.user_id:
                    src_x, src_y = data['src_coordinate'].split("-")
                    dest_x, dest_y = data['coordinate'].split("-")
                    if (src_x, src_y) == (dest_x, dest_y):
                        movable, movable_coordinates = game.select_piece(int(src_x), int(src_y))
                        if movable:
                            message.update({'movable_coordinates': movable_coordinates})
                        action = "select"
                    else:
                        game.move_piece((int(src_x), int(src_y)), (int(dest_x), int(dest_y)))
                        has_winner, winner = game.check_win()
                        if has_winner:
                            action = "Wins!"
                            message.update({"winner": winner})

            board = game.board.serialize()
            print(game.board)
            message.update({
                'action': action,
                'board': board,
                'message': player_name + ": " + action,
                'movable': movable,
                'turn': game.turn.user_id
            })
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.game_id,
            {
                'type': 'broadcast',
                'message': message
            }
        )

    def broadcast(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

    def is_my_turn(self, game, player_id):
        return game.turn == player_id
