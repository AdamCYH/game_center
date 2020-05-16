from game.player import Player


class FiveInARowPlayer(Player):
    def __init__(self, user_id, name):
        super().__init__(user_id, name)
        self.piece_collection = None
