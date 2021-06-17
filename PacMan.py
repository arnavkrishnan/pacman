import pygame
import time

rows = 11
columns = 20
grid_size = 50
grid_x = 0
grid_y = 0
screen = pygame.display.set_mode([columns*grid_size,rows*grid_size])
screen.fill((0,0,0))
pygame.display.set_caption('my first game')
pygame.display.update()

pacman = pygame.image.load('pacman.png')
size = 50
pacman = pygame.transform.scale(pacman, (size, size))

map = [ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 0, 1, 0, 0, 9, 9, 0, 0, 1, 0, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 9, 9, 9, 9, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def draw_player(pacman):
    rect = pacman.get_rect()
    rect.center = (px, py)
    pacman = pygame.transform.rotate(pacman, pa)
    screen.blit(pacman, rect)

def eat_pellets():
    gx = px//grid_size
    gy = py//grid_size
    if map[gy][gx] == 1:
        map[gy][gx] = 3

walls = [[0, 0, 18, 0], [0, 0, 0, 10], [0, 10, 18, 10], [18,0,18,10],
         [2, 2, 3, 2], [2, 2, 2, 4], [5, 0, 5, 2], [4, 4, 5, 4],
         [2, 8, 3, 8], [2, 6, 2, 8], [5, 8, 5, 10], [4, 6, 5, 6],
         [15, 2, 16, 2], [16, 2, 16, 4], [13, 0, 13, 2], [13, 4, 14, 4],
         [15, 8, 16, 8], [16, 6, 16, 8], [13, 8, 13, 10], [13, 6, 14, 6],
         [7, 2, 11,2], [7, 8, 11, 8], [7, 6, 11, 6],
         [7, 4, 8, 4], [10, 4, 11, 4], [7, 4, 7, 6], [11, 4, 11, 6],
         [9, 4, 9, 4]] # last one is the door


def draw_map():
    screen.fill((0, 0, 0))
    for i in range(rows):
        grid_y = i*grid_size
        for j in range(columns):
            grid_x = j*grid_size
            if map[i][j] == 1:
                pygame.draw.circle(screen, "red", (grid_x + grid_size//2, grid_y + grid_size//2), 4)
            #elif map[i][j] == 0:
             #   pygame.draw.rect(screen, "blue", (grid_x, grid_y, grid_size, grid_size))
    draw_walls()

wall_rects = []
def convert_walls():
    for i in range(len(walls)):
        gx1, gy1, gx2, gy2 = walls[i]
        if gx1 == gx2: # vertical wall
            x1 = gx1*grid_size+grid_size//4
            x2 = gx1*grid_size+3*grid_size//4
            y1 = gy1*grid_size+grid_size//4
            y2 = (gy2+1)*grid_size-grid_size//4
        else:
            y1 = gy1*grid_size+grid_size//4
            y2 = gy1*grid_size+3*grid_size//4
            x1 = gx1*grid_size+grid_size//4
            x2 = (gx2+1)*grid_size-grid_size//4
        wall_rects.append((x1, y1, x2, y2))

def draw_walls():
    for i in range(len(wall_rects)-1):
        gx1, gy1, gx2, gy2 = wall_rects[i]
        pygame.draw.rect(screen, "blue", (gx1, gy1, gx2-gx1, gy2-gy1))
    gx1, gy1, gx2, gy2 = wall_rects[len(wall_rects)-1]
    pygame.draw.rect(screen, "pink", (gx1, gy1, gx2-gx1, gy2-gy1))

def collision():
    for k in range(len(wall_rects)):
        if ccr(px, py, size//2, wall_rects[k][0], wall_rects[k][2], wall_rects[k][1], wall_rects[k][3]):
            return True
            print(1)
    return False

def ccr(cx, cy, r, x1, x2, y1, y2):
    x = max(x1, min(cx, x2))
    y = max(y1, min(cy, y2))
    if ((cx-x)*(cx-x)+(cy-y)*(cy-y)) < r*r:
        return True
    else:
        return False

running = True
convert_walls()
#pacman = pacman0
pacman_home_x = 9
pacman_home_y = 7
px = pacman_home_x*grid_size+grid_size//2
py = pacman_home_y*grid_size+grid_size//2
pa = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keypressed = pygame.key.get_pressed()
    #pacman = pacman0
    if keypressed[pygame.K_LEFT]:
        px -= 5
        pa = 180
        if collision():
            px += 5
    if keypressed[pygame.K_RIGHT]:
        px += 5
        pa = 0
        if collision():
            px -= 5
    if keypressed[pygame.K_UP]:
        py -= 5
        pa = 90
        if collision():
            py += 5
    if keypressed[pygame.K_DOWN]:
        py += 5
        pa = -90
        if collision():
            py -= 5

    eat_pellets()
    draw_map()
    draw_player(pacman)
    pygame.display.update()
    pygame.time.Clock().tick(30)
