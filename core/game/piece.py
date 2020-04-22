class PieceCollection:
    def __init__(self):
        self.pieces = None


class Piece:
    # Status 0  Hidden
    # Status 1  Shown

    def __init__(self, player):
        self.animal = None
        self.status = 0
        self.player = player
        self.x = None
        self.y = None

    def flip(self):
        if self.status is 0:
            self.status = 1

    def move(self, dest_x, dest_y):
        pass

    def set_player(self, player):
        self.player = player

    def get_status(self):
        return self.status

    def __str__(self):
        if self.status == 0:
            return "#####"
        return "{}:{}".format(self.player, self.animal)

    def __repr__(self):
        return "{}:{}".format(self.player, self.animal)
