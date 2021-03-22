from Cell import Cell
from Minefield import Grid
from sympy import *
import random as rnd, numpy as np

def basic_agent(mines, queue, better_guess):
    #Counts number of queried and flagged cells for win condition
    count = 0
    
    length = len(queue)
    while queue and count<length:
        count += 1
        cell = queue.pop(0)

        #Tuple representing 1. list of neighboring cells that are not flagged or found bombs, 2. If these neighbors are safe or bombs
        (neighbors, is_safe) = search_neighbors(cell, mines)

        #Can not make a definitive decision based on single cell's information
        if is_safe is None:
            queue.append(cell)
            continue

        #Query neighboring cells or flag neighboring cells
        for nb in neighbors:
            nb.queried = is_safe
            nb.flagged = not is_safe
            #Append safe cells
            if nb.queried:
                queue.append(nb)
        return
    
    #Make a guess if the queue is empty
    guess = None
    if better_guess:
        guess = educated_guess(mines, queue)
    
    if guess is None:
        guess = guess_query(mines)
    if not guess.bomb:
        queue.append(guess)

#Basic agent method but returns True if it can make a definite deduction and false otherwise
def basic_agent_util(mines, queue):
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
        return True
    return False

def advanced_agent(mines, queue, better_guess):
    basic_worked = basic_agent_util(mines, queue)
    
    # in this case, the basic agent was able to make a calculation
    if basic_worked: 
        return

    # Now, create matrix to represent all equations
    tiles = []
    count = 0

    #Key maps from coordinate in mines.field onto the cell in tiles[]
    key = np.ndarray(shape=(mines.dim,mines.dim), dtype=int)
    for i in range(mines.dim):
        for j in range(mines.dim):
            key[i][j]=-1
    for i in range(len(queue)): # adds all of the unique tiles in system of equations to tiles[]
        cell = queue[i]
        for neighbor in mines.neighbors:
            if cell.x + neighbor[0] >= 0 and cell.x + neighbor[0] < mines.dim and cell.y + neighbor[1] >= 0 and cell.y + neighbor[1] < mines.dim:
                nb = mines.field[cell.x + neighbor[0]][cell.y + neighbor[1]]
                if (mines.field[cell.x + neighbor[0]][cell.y + neighbor[1]].queried or mines.field[cell.x + neighbor[0]][cell.y + neighbor[1]].flagged):
                    continue    
                if(key[cell.x + neighbor[0]][cell.y + neighbor[1]]>=0):
                    continue
                tiles.append(nb)
                key[cell.x + neighbor[0]][cell.y + neighbor[1]] = count
                count = count+1
    
    system_matrix = np.ndarray(shape=(len(queue),count+1))
    for i in range(len(queue)):
        for j in range(count+1):
            system_matrix[i][j] = 0
    for i in range(len(queue)): # adds all of the systems of equations into system_matrix
        cell = queue[i]
        n = cell.num_bombs
        for neighbor in mines.neighbors:
            x = cell.x + neighbor[0]
            y = cell.y + neighbor[1]
            if cell.x + neighbor[0] >= 0 and cell.x + neighbor[0] < mines.dim and cell.y + neighbor[1] >= 0 and cell.y + neighbor[1] < mines.dim:
                #Subtracts num of cells left for each discovered bomb
                if mines.field[cell.x + neighbor[0]][cell.y + neighbor[1]].queried:
                    if(mines.field[cell.x + neighbor[0]][cell.y + neighbor[1]].bomb):
                        n = n-1
                    continue
                if mines.field[cell.x + neighbor[0]][cell.y + neighbor[1]].flagged:
                    n = n-1
                    continue

                #Now an uncovered tile
                tile = tiles[key[x][y]] 
                system_matrix[i][key[x][y]] = 1

        # n is now equal to number of undiscovered mines
        system_matrix[i][count] = n
  
    #If count is zero, there are no undiscovered tiles within neighbors of the queue
    if count>0: 
        rref = Matrix(system_matrix)
        #Compute reduced row echelon form of the matrix
        rref = rref.rref()
        
        new_matrix = np.array(rref[0], dtype=float)
        
        for i in range(len(queue)):
            #sum of positive and negative values in row i respectively
            posval = 0
            negval = 0
            for j in range(count):
                if new_matrix[i][j]>0: posval = posval+new_matrix[i][j]
                else: negval = negval+new_matrix[i][j]
            val = new_matrix[i][count]

            #In the case that all values are zero, nothing can be inferred
            if val==0 and posval==0 and negval==0:
                continue
            
            #Only solution is when all positive values correspond to 1s and negative values are 0s
            if(val==posval):
                for j in range(count):
                    if(new_matrix[i][j]>0): tiles[j].flagged = True
                    elif(new_matrix[i][j]<0):
                        tiles[j].queried = True
                        if not tiles[j].bomb: queue.append(tiles[j])
                return

            #Solution is when all positive values correspond to 0s and negative values are 1s
            elif(val==negval):
                for j in range(count):
                    if(new_matrix[i][j]<0): tiles[j].flagged = True
                    elif(new_matrix[i][j]>0):
                        tiles[j].queried = True
                        if not tiles[j].bomb: queue.append(tiles[j])
                return
    
    #Otherwise make a guess
    guess = None
    if better_guess:
        guess = educated_guess(mines, queue)
    if guess is None:
        guess = guess_query(mines)
    if not guess.bomb:
        queue.append(guess)

#Randomly queries the least likely bomb from nearby neighbors
def educated_guess(mines, queue):
    if not queue:
        return None
    least = None
    for cell in queue:
        if not least:
            least = cell
        else:
            cell_info = get_bombs_left(mines, cell)
            least_info =  get_bombs_left(mines, least)
            cell_percent = cell_info[1]/(cell_info[1] + cell_info[0])
            least_percent = least_info[1]/(least_info[0] + least_info[1])

            least = cell if cell_percent > least_percent else least
    
    query = random_neighbor(mines, least)
    query.queried = True

    return query

def random_neighbor(mines, cell):
    neighbor = mines.neighbors[rnd.randint(0, len(mines.neighbors) - 1)]
    while cell.x + neighbor[0] < 0 or cell.x + neighbor[0] >= mines.dim or cell.y + neighbor[1] < 0 or cell.y + neighbor[1] >= mines.dim:
        neighbor = mines.neighbors[rnd.randint(0, len(mines.neighbors) -1 )]

    return mines.field[cell.x + neighbor[0]][cell.y + neighbor[1]]

#returns the number of bombs and cells remaining
def get_bombs_left(mines, cell):
    bombs = cell.num_bombs
    safe = cell.num_safe
    for neighbor in mines.neighbors:
        if cell.x + neighbor[0] >= 0 and cell.x + neighbor[0] < mines.dim and cell.y + neighbor[1] >= 0 and cell.y + neighbor[1] < mines.dim:
            nb = mines.field[cell.x + neighbor[0]][cell.y + neighbor[1]]    
            if nb.flagged or (nb.queried and nb.bomb):
                bombs -= 1
            if (nb.queried and not nb.bomb):
                safe -= 1

    return (bombs, safe)

def guess_query(mines):
    rand_x = rnd.randint(0, mines.dim - 1)
    rand_y = rnd.randint(0, mines.dim - 1)
    
    #Finds cells that are unqueried and unflagged
    while mines.field[rand_x][rand_y].queried or mines.field[rand_x][rand_y].flagged:
        rand_x = rnd.randint(0, mines.dim - 1)
        rand_y = rnd.randint(0, mines.dim - 1)

    #Queries random cell
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