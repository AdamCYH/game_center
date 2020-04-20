class Player:

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.ready = False
        self.my_turn = False
        return

    def change_status(self):
        self.ready = not self.ready

    def __str__(self):
        return self.name
