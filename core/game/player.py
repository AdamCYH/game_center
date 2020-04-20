class Player:

    def __init__(self):
        self.id = ""
        self.name = ""
        self.ready = False
        self.my_turn = False
        return

    def change_status(self):
        self.ready = not self.ready

    def __set_name__(self, owner, name):
        self.name = name

    def __str__(self):
        return self.name

