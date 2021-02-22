class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bomb = False
        self.clicked = False

        self.num_bombs = 0


    def __str__(self):
        return '({self.x}, {self.y})'.format(self=self)

    def __repr__(self):
        return '({self.x}, {self.y}) {self.bomb}'.format(self=self)