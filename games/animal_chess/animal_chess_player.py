from games.player import Player


class AnimalChessPlayer(Player):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.piece_collection = None
