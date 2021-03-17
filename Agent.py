from Cell import Cell
from Minefield import Grid
import random as rnd, numpy as np

def basic_agent(mines, queue):
    count = 0
    length = len(queue)
    while queue and count<length:
        count += 1
        cell = queue.pop(0)
        (neighbors, is_safe) = search_neighbors(cell, mines)
        if is_safe is None:
            queue.append(cell)
            continue
        for nb in neighbors:
            nb.queried = is_safe
            nb.flagged = not is_safe
            if nb.queried:
                queue.append(nb)
        return 
    
    guess = guess_query(mines)
    if not guess.bomb:
        queue.append(guess)

def guess_query(mines):
    rand_x = rnd.randint(0, mines.dim - 1)
    rand_y = rnd.randint(0, mines.dim - 1)
    
    while mines.field[rand_x][rand_y].queried or mines.field[rand_x][rand_y].flagged:
        rand_x = rnd.randint(0, mines.dim - 1)
        rand_y = rnd.randint(0, mines.dim - 1)

    mines.field[rand_x][rand_y].queried = True
    return mines.field[rand_x][rand_y]

def search_neighbors(cell, mines):
    n = cell.num_bombs
    safe_neighbors = []

    #Check surrounding neighbors of queried cell
    for neighbor in mines.neighbors:
        if cell.x + neighbor[0] >= 0 and cell.x + neighbor[0] < mines.dim and cell.y + neighbor[1] >= 0 and cell.y + neighbor[1] < mines.dim:
            nb = mines.field[cell.x + neighbor[0]][cell.y + neighbor[1]]
            if not (nb.queried or nb.flagged):
                safe_neighbors.append(nb)
            elif nb.flagged or (nb.queried and nb.bomb):
                n -= 1
    
    #Case that all bombs are found in neighbors and the list contains safe cells
    if n==0:
        return (safe_neighbors, True)
    #Case that every surrounding nonqueried is a bomb
    if n==len(safe_neighbors):
        return (safe_neighbors, False)
    #Case that no decisions can be made from the information of this cell
    return (None,None)