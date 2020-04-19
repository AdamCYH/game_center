class Player:
    def __init__(self):
        self.status = 'not ready'
        return

    def change_status(self):
        if self.status == 'ready':
            self.status = 'not ready'
        else:
            self.status = 'ready'
