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
            
            mine_cnt -= 1

    def set_info(self):
        for i in range(self.dim):
            for j in range(self.dim):
                if not self.field[i][j].bomb:
                    for neighbor in self.neighbors:
                        if i + neighbor[0] >= 0 and i + neighbor[0] < self.dim and j + neighbor[1] >= 0 and j + neighbor[1] < self.dim:
                            nb = self.field[i + neighbor[0]][j + neighbor[1]]
                            if nb.bomb:
                                self.field[i][j].num_bombs += 1
                            else:
                                self.field[i][j].num_safe += 1
    def __init__(self, dim, mines):
        self.dim = dim
        self.num_mines = mines
        self.neighbors = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        self.field = [[Cell(x, y) for x in range(self.dim)] for y in range(self.dim)]
        self.set_mines()
        self.set_info()

        


        