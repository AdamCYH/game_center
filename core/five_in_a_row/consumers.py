import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from core.five_in_a_row.views import games, start_new_game
from games.five_in_a_row.fiar_player import FiveInARowPlayer


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
        print("Receive:", text_data)
        data = json.loads(text_data)
        action = data['action']
        player_name = data['player_name']
        player_id = data['player_id']
        board = []
        message = {}
        if action == 'chat':
            message.update({
                'action': action,
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
                    message.update({game.player1.user_id: game.player1.piece_collection.name,
                                    game.player2.user_id: game.player2.piece_collection.name})
            elif action == 'join':
                pass
            elif action == 'reconnect':
                pass
            elif action == 'establish':
                if player_id == game.turn.user_id:
                    x, y = data['coordinate'].split("-")
                    place_successful, x, y = game.place_piece(int(x), int(y))
                    message.update({'place_successful': place_successful})
                    if place_successful:
                        has_winner, winner = game.check_win((x, y))
                        if has_winner:
                            action = "Wins!"
                            if winner is None:
                                message.update({"winner": "TIE!!"})
                            else:
                                message.update({"winner": winner.name})

                    message.update({'coordinate': [x, y]})
            elif action == 'play_again':
                game = start_new_game(player_name, player_id)
                games[game.id] = game
                message.update({'game_id': game.id})

            board = game.board.serialize()
            print(game.board)
            message.update({
                'action': action,
                'board': board,
                'message': player_name + ": " + action,
                'turn': game.turn.user_id,
                'player_id': player_id,
                'player_name': player_name
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
