from Cell import Cell
import random as rnd
class Grid:
    
    def set_mines(self):

        if self.num_mines > self.dim ** 2:
            print('Illegal number of mines')
            self.num_mines = self.dim ** 2
        mine_cnt = self.num_mines

        while mine_cnt > 0:
            rand_x = rnd.randint(0, self.dim - 1)
            rand_y = rnd.randint(0, self.dim - 1)

            if self.field[rand_x][rand_y].bomb:
                continue

            self.field[rand_x][rand_y].bomb = True
            for neighbor in self.neighbors:
                temp_x = rand_x + neighbor[0]
                temp_y = rand_y + neighbor[1]
                if temp_x >= 0 and temp_x < self.dim and temp_y >= 0 and temp_y < self.dim:
                    self.field[temp_x][temp_y].num_bombs += 1
            mine_cnt -= 1

    def __init__(self, dim, mines):
        self.dim = dim
        self.num_mines = mines
        self.neighbors = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.field = [[Cell(x, y) for x in range(self.dim)] for y in range(self.dim)]
        self.set_mines()

        


        