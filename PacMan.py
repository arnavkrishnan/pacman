import pygame
import time

rows = 4
columns = 20
grid_size = 50
grid_x = ()
grid_y = ()
screen = pygame.display.set_mode([columns*grid_size,rows*grid_size])
screen.fill((0,0,0))
pygame.display.set_caption('my first game')
pygame.display.update()

pacman = pygame.image.load('pacman.png')
size = 1
pacman = pygame.transform.scale(pacman, (size, size))

map = [ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 2, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

def draw_player(pacman):
    rect = pacman.get_rect()
    px = 3*grid_size+grid_size//2
    py = 3*grid_size+grid_size//2
    pa = 0
    rect.center = (px, py)
    screen.blit(pacman, (0, 0))


def draw_map():
    screen.fill((0, 0, 0))
    for i in range(rows):
        grid_y = i*grid_size
        for j in range(columns):
            grid_x = j*grid_size
            if map[i][j] == 1:
                pygame.draw.circle(screen, "red", (grid_x + grid_size//2, grid_y + grid_size//2), 4)
            elif map[i][j] == 0:
                pygame.draw.rect(screen, "blue", (grid_x, grid_y, grid_size, grid_size))

walls = []
wall_rects = []
def convert_walls():
    for i in range(len(walls)):
        gx1, gx2, gy1, gy2 = walls[i]
        if gx1 == gx2:
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
    for i in range(len(wall_rects)):
        gx1, gy1, gx2, gy2 = wall_rects[i]
        pygame.draw.rect(screen, "blue", (gx1, gy1, gx2-gx1, gy2 - gy1))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        draw_map()
        draw_player(pacman)
        pygame.display.update()
        pygame.time.Clock().tick(30)
