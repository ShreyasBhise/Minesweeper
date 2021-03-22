from Cell import Cell
from Minefield import Grid
import Agent as a, numpy as np
import matplotlib.pyplot as plt

def count_safe_bomb(grid):
    safe_query = 0
    for i in range(map_dim):
        for j in range(map_dim):
            if grid.field[i][j].bomb and grid.field[i][j].flagged:
                safe_query += 1
    return safe_query

def count_moves(grid):
    queried = 0
    for i in range(map_dim):
        for j in range(map_dim):
            if grid.field[i][j].flagged or grid.field[i][j].queried:
                queried += 1
    return queried

def reset_board(grid):
    for i in range(map_dim):
        for j in range(map_dim):
            grid.field[i][j].queried = False
            grid.field[i][j].flagged = False


map_dim = 30
density = [ 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
basic = []
advanced = []



for i in density:
    num_bombs = int(i * (map_dim ** 2))
    successA = 0
    successB = 0
    for _ in range(3):
        map = Grid(map_dim, num_bombs)

        #Solve 5 times with basic agent and 5 times with advanced agent
        for j in range(3):
            queue = []
            while count_moves(map) != map_dim ** 2:
               a.basic_agent(map, queue, False)
               
            successB += count_safe_bomb(map)
            reset_board(map)
            print('B:', i, j, successB, num_bombs)
        for j in range(3):
            queue = []
            while count_moves(map) != map_dim ** 2:
                a.advanced_agent(map, queue, False)
            
            successA += count_safe_bomb(map)
            reset_board(map)
            print('A:',i, j, successA, num_bombs)
    
    basic.append(successB/(num_bombs *9 ))
    advanced.append(successA/(num_bombs * 9))

print(basic)
print(advanced)

plt.title('Basic vs. Advanced - Size = 20')
plt.plot(density, basic, '-ro', label = 'Basic')
plt.plot(density, advanced, '-bo', label = 'Advanced')
plt.legend()

plt.xlabel('Mine Density')
plt.ylabel('Average Score - 5 tests/minefield')
plt.show()