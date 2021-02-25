from Minefield import Grid
from Cell import Cell
import pygame, pprint, sys


def update_ui():
    for i in range(dim):
        for j in range(dim):
            pygame.draw.rect(screen,(255,255,255), (i*(width/dim), j*(height/dim), width/dim, height/dim))
            
            if not mines.field[i][j].clicked:
                if mines.field[i][j].flagged:
                    pygame.draw.rect(screen,(255,128,0), (i*(width/dim), j*(height/dim), width/dim, height/dim))
                    
                    text = font.render('B', True, (0, 0, 0))
                    rect = text.get_rect()
                    rect.center = (i*(width/dim) + (width/(2*dim)), j*(height/dim) + (height/(2*dim)))
                    screen.blit(text, rect)
                else:
                    pygame.draw.rect(screen,(128,128,128), (i*(width/dim), j*(height/dim), width/dim, height/dim))
                    
                    text = font.render('?', True, (0, 0, 0))
                    rect = text.get_rect()
                    rect.center = (i*(width/dim) + (width/(2*dim)), j*(height/dim) + (height/(2*dim)))
                    screen.blit(text, rect)
                
            elif mines.field[i][j].bomb:
                pygame.draw.rect(screen,(255,0,0), (i*(width/dim), j*(height/dim), width/dim, height/dim))
            elif mines.field[i][j].num_bombs == 0:
                pygame.draw.rect(screen,(0, 255,0), (i*(width/dim), j*(height/dim), width/dim, height/dim))

                text = font.render('C', True, (0, 0, 0))
                rect = text.get_rect()
                rect.center = (i*(width/dim) + (width/(2*dim)), j*(height/dim) + (height/(2*dim)))
                screen.blit(text, rect)
            
            else:
                text = font.render(str(mines.field[i][j].num_bombs), True, (0, 0, 0))
                rect = text.get_rect()
                rect.center = (i*(width/dim) + (width/(2*dim)), j*(height/dim) + (height/(2*dim)))
                screen.blit(text, rect)
            pygame.draw.rect(screen,(0,0,0), (i*(width/dim), j*(height/dim), width/dim, height/dim), 1)
    pygame.display.flip()
def get_clicked_pos(pos):
    gap = width // dim
    return pos[0] // gap, pos[1]//gap
dim = 10
num_mines = 14

size = width, height = 800, 800 

screen = pygame.display.set_mode(size)
mines = Grid(dim, num_mines)


pygame.init()
font = pygame.font.SysFont('arial', 50)
pprint.pprint(mines)
update_ui()

while True:
    pygame.time.Clock().tick(144)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if pygame.mouse.get_pressed()[0]:
            pos = get_clicked_pos(pygame.mouse.get_pos())
            mines.field[pos[0]][pos[1]].clicked = True
            update_ui()
        if pygame.mouse.get_pressed()[2]:
            pos = get_clicked_pos(pygame.mouse.get_pos())
            mines.field[pos[0]][pos[1]].flagged = True
            update_ui()
