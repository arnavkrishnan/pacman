import pygame
pygame.init()
import random

grid_size = 50
rows = 11
columns = 19
screen_width = columns*grid_size
screen_height = (rows+1)*grid_size
screen = pygame.display.set_mode([screen_width, screen_height]) # size of screen
screen.fill('black')
size = grid_size-6
pacman0 = pygame.image.load('pacman.png')
pacman0 = pygame.transform.scale(pacman0, (size, size))
blinkly = pygame.image.load('blinkly.png')
blinkly = pygame.transform.scale(blinkly, (size, size))
pinky = pygame.image.load('pinky.png')
pinky = pygame.transform.scale(pinky, (size, size))
inky = pygame.image.load('inky.png')
inky = pygame.transform.scale(inky, (size, size))

map =  [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,2,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,2,0],
		[0,1,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,1,0],
		[0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0],
		[0,1,0,1,0,0,1,0,0,9,0,0,1,0,0,1,0,1,0],
		[0,1,1,1,1,1,1,0,9,9,9,0,1,1,1,1,1,1,0],
		[0,1,0,1,0,0,1,0,0,0,0,0,1,0,0,1,0,1,0],
		[0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0],
		[0,1,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0,1,0],
		[0,2,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,2,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

walls = [[0, 0, 18, 0], [0, 0, 0, 10], [0, 10, 18, 10], [18,0,18,10],
		 [2, 2, 3, 2], [2, 2, 2, 4], [5, 0, 5, 2], [4, 4, 5, 4],
		 [2, 8, 3, 8], [2, 6, 2, 8], [5, 8, 5, 10], [4, 6, 5, 6],
		 [15, 2, 16, 2], [16, 2, 16, 4], [13, 0, 13, 2], [13, 4, 14, 4],
		 [15, 8, 16, 8], [16, 6, 16, 8], [13, 8, 13, 10], [13, 6, 14, 6],
		 [7, 2, 11,2], [7, 8, 11, 8], [7, 6, 11, 6],
		 [7, 4, 8, 4], [10, 4, 11, 4], [7, 4, 7, 6], [11, 4, 11, 6],
		 [9, 4, 9, 4]] # last one is the door

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

def draw_map():
	screen.fill('black')
	for i in range(rows):
		grid_y = i*grid_size
		for j in range(columns):
			grid_x = j*grid_size
			if map[i][j] == 1:
				pygame.draw.circle(screen, "red", (grid_x+grid_size//2, grid_y+grid_size//2), 4)
			if map[i][j] == 2:
				pygame.draw.circle(screen, "pink", (grid_x+grid_size//2, grid_y+grid_size//2), 12)
	draw_walls()

def draw_pacman(pacman):
	rect = pacman.get_rect()
	rect.center = (p_x, p_y)
	screen.blit(pacman, rect)

def draw_ghost(ghost, g_x, g_y):
	rect = ghost.get_rect()
	rect.center = (g_x, g_y)
	screen.blit(ghost, rect)


def eat_pellets():
	global pellet_count
	global power_up
	g_x = p_x//grid_size
	g_y = p_y//grid_size
	if map[g_y][g_x] == 1:
		map[g_y][g_x] = -1
		pellet_count += 1
	elif map[g_y][g_x] == 2:
		map[g_y][g_x] = -1
		power_up = 2

def draw_text(text,size, cx, cy):
	font = pygame.font.Font('freesansbold.ttf',size)
	bigtext = font.render(text, True, (255,255,255))
	textrect = bigtext.get_rect()
	textrect.center = (cx,cy)
	screen.blit(bigtext, textrect)

def collide_circle_rect(cx, cy, r, x1, x2, y1, y2):
	x = max(x1, min(cx, x2))
	y = max(y1, min(cy, y2))
	if ((cx-x)*(cx-x)+(cy-y)*(cy-y)) < r*r:
		return True
	else:
		return False

def check_collision(): # check pacman's collision with walls - pacman is at p_x, py
	for k in range(len(wall_rects)):
		if collide_circle_rect(p_x, p_y, size//2, wall_rects[k][0], wall_rects[k][2], wall_rects[k][1], wall_rects[k][3]):
			return True
	return False

def move_ghost(ghost, cx, cy, dx, dy):
	cx += 2*dx
	cy += 2*dy
	return (cx, cy)

d_x = [0, -1, 0, 1]
d_y = [-1, 0, 1, 0]

def next_goal_chase(c_x, c_y, c_d, p_x, p_y):
	# select the next point to move to depending on where Pacman is
	# ghost can not reverse travel direction
	grid_x = c_x//grid_size
	grid_y = c_y//grid_size
	del_x = (p_x - c_x)//5 # relative to pacman
	del_y = (p_y - c_y)//5
	preferred_direction = []
	direction = []
	if del_x != 0:
		del_x = del_x/abs(del_x)
	if del_y != 0:
		del_y = del_y/abs(del_y)

	if c_d > -1:
		bad_d = (c_d + 2)%4 # can not reverse direction
	else:
		bad_d = -1 # no bad direction in the beginning

	for k in range(4):
		r = grid_y+d_y[k]
		c = grid_x+d_x[k]
		if k != bad_d and (map[r][c] == 1 or map[r][c] == 2 or map[r][c] == -1) and \
			not (r == b_y//grid_size and c == b_x//grid_size) and \
			not (r == n_y//grid_size and c == n_x//grid_size):
			c_d = k # direction of travel
			g_x = c*grid_size+grid_size//2
			g_y = r*grid_size+grid_size//2
			if (del_x == 0 and del_y == d_y[k]) or (del_y == 0 and del_x == d_x[k]) or \
			(del_x != 0 and del_y != 0 and (d_x[k] == del_x or d_y[k] == del_y)):
				preferred_direction.append((g_x, g_y, c_d, d_x[k], d_y[k]))
			direction.append((g_x, g_y, c_d, d_x[k], d_y[k]))

	if (len(preferred_direction) > 0):
		return preferred_direction[random.randint(0, len(preferred_direction)-1)]
	elif (len(direction) > 0):
		return direction[random.randint(0, len(direction)-1)]
	else:
		return False

def find_pinky_target(p_x, p_y, p_a):
	#find two grid ahead of pacman
	t_x_g = p_x//grid_size
	t_y_g = p_y//grid_size
	if p_a == 0: #pacman heading right
		t_x_g += 4
	if p_a == 180:
		t_x_g -= 4
	if p_a == 90: #pacman heading up
		t_y_g -= 4
	if p_a == 270:
		t_y_g += 4
	return t_x_g, t_y_g

def find_inky_target(p_x, p_y, p_a):
	#find two grid ahead of pacman
	t_x_g = p_x//grid_size
	t_y_g = p_y//grid_size
	if p_a == 0: #pacman heading right
		t_x_g += 2
	if p_a == 180:
		t_x_g -= 2
	if p_a == 90: #pacman heading up
		t_y_g -= 2
	if p_a == 270:
		t_y_g += 2
	b_x_g = b_x//grid_size
	b_y_g = b_y//grid_size
	del_x = t_x_g - b_x_g
	del_y = t_y_g - b_y_g
	t_x_g += del_x
	t_y_g += del_y
	return t_x_g, t_y_g

def same_grid(p_x, py, g_x, g_y):
	c_x1 = p_x // grid_size
	c_y1 = p_y // grid_size
	c_x2 = g_x // grid_size
	c_y2 = g_y // grid_size
	if c_x1 == c_x2 and c_y1 == c_y2:
		return True
	else:
		return False

running = True
pacman = pacman0
pacman_home_x = 9
pacman_home_y = 7
p_x = pacman_home_x*grid_size+grid_size//2
p_y = pacman_home_y*grid_size+grid_size//2
p_a = 0

#blinkly
blinkly_home_x = 9
blinkly_home_y = 3
b_x = blinkly_home_x*grid_size+grid_size//2
b_y = blinkly_home_y*grid_size+grid_size//2
b_d = -1 # travel direction, initially none

gb_x = b_x
gb_y = b_y
db_x = 0
db_y = 0

#pinky
pinky_home_x = 9
pinky_home_y = 5
n_x = pinky_home_x*grid_size+grid_size//2
n_y = pinky_home_y*grid_size+grid_size//2
n_d = -1 # travel direction

gn_x = n_x
gn_y = n_y
dn_x = 0
dn_y = 0
pinky_in_house = True

#inky
inky_home_x = 10
inky_home_y = 5
i_x = inky_home_x*grid_size+grid_size//2
i_y = inky_home_y*grid_size+grid_size//2
i_d = -1 # travel direction

gi_x = i_x
gi_y = i_y
di_x = 0
di_y = 0
inky_in_house = True

p_speed = 3
g_speed = 2

pellet_count = 0
power_up = 0
convert_walls()
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	keypressed = pygame.key.get_pressed()  #getting all the keys that are pressed
	if keypressed[pygame.K_LEFT]:
		if p_a != 180:
			pacman = pygame.transform.flip(pacman0, True, False)
		p_a = 180
		p_x -= p_speed
		if check_collision():
			p_x += p_speed
	if keypressed[pygame.K_RIGHT]:
		if p_a != 0:
			pacman = pacman0
		p_a = 0
		p_x += p_speed
		if check_collision():
			p_x -= p_speed
	if keypressed[pygame.K_UP]:
		if p_a != 90:
			pacman = pygame.transform.rotate(pacman0, 90)
			p_a = 90
		p_y -= p_speed
		if check_collision():
			p_y += p_speed
	if keypressed[pygame.K_DOWN]:
		if p_a != 270:
			pacman = pygame.transform.rotate(pacman0, 90)
			pacman = pygame.transform.flip(pacman, False, True)
			p_a = 270
		p_y += p_speed
		if check_collision():
			p_y -= p_speed

	eat_pellets()
	draw_map()
	draw_pacman(pacman)

	#blinkly
	if abs(b_x-gb_x)+abs(b_y-gb_y) > 4:
		where_blinkly = move_ghost(blinkly, b_x, b_y, db_x, db_y)
		b_x = where_blinkly[0]
		b_y = where_blinkly[1]
	else:
		next_pos = next_goal_chase(b_x, b_y, b_d, p_x, p_y)
		if next_pos != False:
			gb_x, gb_y, b_d, db_x, db_y = next_pos

	# pinky
	if pinky_in_house:
		if (b_x//grid_size != blinkly_home_x) or (b_y//grid_size != blinkly_home_y):
			n_x = blinkly_home_x*grid_size+grid_size//2
			n_y = blinkly_home_y*grid_size+grid_size//2
			n_d = -1 # travel direction
			gn_x = n_x
			gn_y = n_y
			dn_x = 0
			dn_y = 0
			pinky_in_house = False
	if abs(n_x-gn_x)+abs(n_y-gn_y) > 4:
		where_pinky = move_ghost(pinky, n_x, n_y, dn_x, dn_y)
		n_x = where_pinky[0]
		n_y = where_pinky[1]
	else:
		t_x,t_y = find_pinky_target(p_x, p_y, p_a)
		t_x = t_x * grid_size
		t_y = t_y * grid_size
		next_pos = next_goal_chase(n_x, n_y, n_d, t_x, t_y)
		if next_pos != False:
			gn_x, gn_y, n_d, dn_x, dn_y = next_pos

	ix, iy = find_inky_target(p_x, p_y, p_a)

	draw_ghost(blinkly, b_x, b_y)
	draw_ghost(pinky, n_x, n_y)
	draw_ghost(inky, i_x, i_y)

	if same_grid(p_x, p_y, b_x, b_y) or same_grid(p_x, p_y, n_x, n_y):
		pygame.time.wait(1000)
		p_x = 9*grid_size+grid_size//2
		p_y = 7*grid_size+grid_size//2
		p_a = 0
		pacman = pacman0
		b_x = blinkly_home_x*grid_size+grid_size//2
		b_y = blinkly_home_y*grid_size+grid_size//2
		b_d = -1 # travel direction, initially
		gb_x = b_x
		gb_y = b_y
		db_x = 0
		db_y = 0

		n_x = pinky_home_x*grid_size+grid_size//2
		n_y = pinky_home_y*grid_size+grid_size//2
		n_d = -1 # travel direction, initially
		gn_x = n_x
		gn_y = n_y
		dn_x = 0
		dn_y = 0
		pinky_in_house = True

	draw_text("score: "+str(pellet_count), 30, screen_width//2, screen_height - grid_size//2)

	pygame.display.flip()
	ticks_passed = pygame.time.Clock().tick(30)


pygame.quit()
