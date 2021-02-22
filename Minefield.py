from Cell import Cell
import random as rnd
class Grid:

    def set_mines(self):

        if self.num_mines > self.dim ** 2:
            print('Illegal number of mines')
            self.num_mines = self.dim ** 2
        temp = self.num_mines

        while temp > 0:
            rand_x = rnd.randint(0, self.dim - 1)
            rand_y = rnd.randint(0, self.dim - 1)

            if self.field[rand_x][rand_y].bomb:
                continue

            self.field[rand_x][rand_y].bomb = True
            temp -= 1

    def __init__(self, dim, mines):
        self.dim = dim
        self.num_mines = mines
        self.field = [[Cell(x, y) for x in range(self.dim)] for y in range(self.dim)]
        self.set_mines()


        