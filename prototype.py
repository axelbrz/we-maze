import sys
import pygame
import pygame.gfxdraw
import time
import random
import os

def bfs(ini, end):
	# de p2 a p1
	dx = [0, 0, -1, 1]
	dy = [-1, 1, 0, 0]
	
	if ini == end:
		print "Done"
		return []
	
	q = [ini]
	used = set(ini)
	pre = {}
	i = 0
	while len(q) - i > 0:
		c = q[i]
		for j in xrange(4):
			n = (c[0] + dx[j], c[1] + dy[j])
			if not n in used and empty(n[0], n[1]):
				used.add(n)
				pre[n] = c
				q.append(n)
				if n == end:
					break
		i += 1
	
	path = [end]
	c = end
	while (c in pre) and c != ini:
		#print path
		path.append(pre[c])
		c = pre[c]
	return path[::-1][1:]

def bfs_p2_to_p1():
	return bfs((p2[0], p2[1]), (p1[0], p1[1]))
	
def bfs_p1_to_p2():
	return bfs((p1[0], p1[1]), (p2[0], p2[1]))


def loadMaze(maze):
	global p1, p2, m, images
	
	p1 = None
	p2 = None
	images = []
	imagePool = [
		#edificio_1,
		#edificio_2,
		edificio_3,
		edificio_4,
		edificio_5,
		edificio_6,
		plaza,
	]
	print "--"
	m = maze.split("\n")[0:-1]
	for y in xrange(len(m)):
		x1 = m[y].find("1")
		x2 = m[y].find("2")
		if x1 >= 0: p1 = [x1, y]
		if x2 >= 0: p2 = [x2, y]
		m[y] = m[y].replace("1", " ")
		m[y] = m[y].replace("2", " ")
		images.append([random.choice(imagePool) for x in xrange(len(m[0]))])
		print "".join(m[y])
	print "--"
	print "Dimensiones", (len(m[0]), len(m))
	print p1, p2
	m = [[c for c in row] for row in m]

def empty(x, y):
	global m
	if x < 0 or y < 0 or x >= len(m[0]) or y >= len(m): return False
	return m[y][x] == " "

def filled(x, y):
	global m
	if x < 0 or y < 0 or x >= len(m[0]) or y >= len(m): return False
	return m[y][x] == "X" or m[y][x] == "O"

def isMovable(c):
	if empty(c[0], c[1]-1) and empty(c[0], c[1]+1):
		if filled(c[0]-1, c[1]) and filled(c[0]+1, c[1]):
			return True
	if filled(c[0], c[1]-1) and filled(c[0], c[1]+1):
		if empty(c[0]-1, c[1]) and empty(c[0]+1, c[1]):
			return True
	return False

def dist(a, b):
	return abs(a[0]-b[0]) + abs(a[1]-b[1])

def alterMaze():
	path = bfs_p1_to_p2() # minpath
	if len(path) < 5: # VARIABLE DE CONFIG!!
		print "Maze not altered as they almost win..."
		return
	print "Altering maze..."
	
	for i in xrange(100):
		torem = 1 + int(random.random() * (len(m[0])-1)), 1 + int(random.random() * (len(m)-1)) # x, y
		if m[torem[1]][torem[0]] != "X": continue
		toadd = path[int(random.random() * len(path))]
		if dist(toadd, p1) == 0 or dist(toadd, p2) == 0: continue # VARIABLES DE CONFIG!!
		if list(p1) == list(toadd) or list(p2) == list(toadd): continue
		
		if isMovable(torem) and isMovable(toadd):
			m[torem[1]][torem[0]] = " "
			m[toadd[1]][toadd[0]] = "X"
			newpath = bfs_p2_to_p1()
			if len(newpath) > 0:
				return
			else:
				m[torem[1]][torem[0]] = "X"
				m[toadd[1]][toadd[0]] = " "

def getDrawPos(x, y):
	global wallsize
	return (x * wallsize + 0, y * wallsize + 0, wallsize - 0, wallsize - 0)

def drawAsfalto(x, y):
	pos = getDrawPos(x, y)
	img = None
	# Linea
	if empty(x-1, y) and empty(x+1, y) and not empty(x, y+1) and not empty(x, y-1):
		img, img_size = pygame.transform.rotate(asfalto_linea, 90), asfalto_size
	if not empty(x-1, y) and not empty(x+1, y) and empty(x, y+1) and empty(x, y-1):
		img, img_size = asfalto_linea, asfalto_size
	
	# Esquina
	if empty(x-1, y) and not empty(x+1, y) and not empty(x, y+1) and empty(x, y-1):
		img, img_size = pygame.transform.rotate(asfalto_esquina, 180), asfalto_size
	if empty(x-1, y) and not empty(x+1, y) and empty(x, y+1) and not empty(x, y-1):
		img, img_size = pygame.transform.rotate(asfalto_esquina, 270), asfalto_size
	if not empty(x-1, y) and empty(x+1, y) and not empty(x, y+1) and empty(x, y-1):
		img, img_size = pygame.transform.rotate(asfalto_esquina, 90), asfalto_size
	if not empty(x-1, y) and empty(x+1, y) and empty(x, y+1) and not empty(x, y-1):
		img, img_size = asfalto_esquina, asfalto_size
	
	# Cruz
	if empty(x-1, y) and empty(x+1, y) and empty(x, y+1) and empty(x, y-1):
		img, img_size = asfalto_cruz, asfalto_size
	
	# Fin
	if empty(x-1, y) and not empty(x+1, y) and not empty(x, y+1) and not empty(x, y-1):
		img, img_size = pygame.transform.rotate(asfalto_fin, 270), asfalto_size
	if not empty(x-1, y) and empty(x+1, y) and not empty(x, y+1) and not empty(x, y-1):
		img, img_size = pygame.transform.rotate(asfalto_fin, 90), asfalto_size
	if not empty(x-1, y) and not empty(x+1, y) and empty(x, y+1) and not empty(x, y-1):
		img, img_size = asfalto_fin, asfalto_size
	if not empty(x-1, y) and not empty(x+1, y) and not empty(x, y+1) and empty(x, y-1):
		img, img_size = pygame.transform.rotate(asfalto_fin, 180), asfalto_size
	
	# T
	if not empty(x-1, y) and empty(x+1, y) and empty(x, y+1) and empty(x, y-1):
		img, img_size = pygame.transform.rotate(asfalto_t, 90), asfalto_size
	if empty(x-1, y) and not empty(x+1, y) and empty(x, y+1) and empty(x, y-1):
		img, img_size = pygame.transform.rotate(asfalto_t, 270), asfalto_size
	if empty(x-1, y) and empty(x+1, y) and not empty(x, y+1) and empty(x, y-1):
		img, img_size = pygame.transform.rotate(asfalto_t, 180), asfalto_size
	if empty(x-1, y) and empty(x+1, y) and empty(x, y+1) and not empty(x, y-1):
		img, img_size = asfalto_t, asfalto_size
	
	if img:
		screen.blit(img, (pos[0], pos[1], img_size[0], img_size[1]))

def drawBuilding(x, y):
	pos = getDrawPos(x, y)
	img = None
	#img, img_size = pygame.transform.rotate(asfalto_linea, 90), asfalto_size
	img, img_size = images[y][x], asfalto_size
	if img:
		screen.blit(img, (pos[0], pos[1], img_size[0], img_size[1]))

def loadImage(filename):
	global imagesPath, wallsize
	img = pygame.image.load(imagesPath + filename)
	return pygame.transform.scale(img, (wallsize, wallsize))

def angleFromDir(dir):
	if dir[0] == 0 and dir[1] == 1: return 90
	if dir[0] == 1 and dir[1] == 0: return 180
	if dir[0] == 0 and dir[1] == -1: return 270
	if dir[0] == -1 and dir[1] == 0: return 0

imagesPath = "images/"
audioPath = "audio/"
levelsPath = "levels/"
levelsName = "level_%d.txt"
levelFiles = []

if len(sys.argv) != 2:
	lvlFiles = os.listdir(levelsPath)
	levelCount = 1
	levelFiles = []
	while (levelsName % levelCount) in lvlFiles:
		levelFiles.append(levelsName % levelCount)
		levelCount += 1
else:
	levelFiles = [ sys.argv[1] ]
print "Levels:", levelFiles

pygame.init()
pygame.display.set_caption('We Maze!')

pygame.mixer.music.load(audioPath + 'back.ogg')
pygame.mixer.music.play(-1)

p1 = None
p2 = None
dir1 = [1, 0]
dir2 = [-1, 0]
images = []

t_anim = 0.1
steps_to_alter_maze = 5

playBot1 = False
playBot2 = False
showBotPath1 = False
showBotPath2 = False

steps = 0

bulletMode = True

levelIndex = 0

while True:
	wallsize = 32
	
	player_1 = loadImage("player_red.png")
	player_2 = loadImage("player_blue.png")
	
	asfalto_linea = loadImage("asfalto_linea.png")
	asfalto_esquina = loadImage("asfalto_esquina.png")
	asfalto_cruz = loadImage("asfalto_cruz.png")
	asfalto_t = loadImage("asfalto_t.png")
	asfalto_fin = loadImage("asfalto_fin.png")
	
	asfalto_size = asfalto_linea.get_size()
	
	edificio_1 = loadImage("edificio_1.png")
	edificio_2 = loadImage("edificio_2.png")
	edificio_3 = loadImage("edificio_3.png")
	edificio_4 = loadImage("edificio_4.png")
	edificio_5 = loadImage("edificio_5.png")
	edificio_6 = loadImage("edificio_6.png")
	plaza = loadImage("plaza.png")
	
	levelFile = levelsPath + levelFiles[levelIndex]
	print levelFile
	with open(levelFile) as f:
		maze = f.read()
	m = []
	loadMaze(maze)
	
	size = width, height = wallsize * len(m[0]), wallsize * len(m)
	print "Screen size", size

	screen = pygame.display.set_mode(size)
	keys = set()

	d1 = p1[:]
	d2 = p2[:]

	pp1 = p1[:]
	pp2 = p2[:]

	t_prev = time.time()
	path1 = []
	path2 = []
	print "New game..."
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				keys.add(event.key)
				if event.key == pygame.K_ESCAPE:
					sys.exit()
			if event.type == pygame.KEYUP:
				keys.discard(event.key)
				
		t_curr = time.time()
		if t_curr - t_prev >= t_anim:
			pp1 = p1[:]
			pp2 = p2[:]
			
			path2 = bfs_p2_to_p1()
			if playBot2:
				if len(path2) <= 1:
					break
				p2 = list(path2[0])
			else:
				if pygame.K_w in keys:
					dir2 = [0, -1]
					if empty(p2[0], p2[1]-1): p2[1] -= 1
				elif pygame.K_s in keys:
					dir2 = [0, 1]
					if empty(p2[0], p2[1]+1): p2[1] += 1
				elif pygame.K_d in keys:
					dir2 = [1, 0]
					if empty(p2[0]+1, p2[1]): p2[0] += 1
				elif pygame.K_a in keys:
					dir2 = [-1, 0]
					if empty(p2[0]-1, p2[1]): p2[0] -= 1
			
			path1 = bfs_p1_to_p2()
			if playBot1:
				if len(path1) <= 1:
					break
				p1 = list(path1[0])
			else:
				if pygame.K_UP in keys:
					dir1 = [0, -1]
					if empty(p1[0], p1[1]-1): p1[1] -= 1
				elif pygame.K_DOWN in keys:
					dir1 = [0, 1]
					if empty(p1[0], p1[1]+1): p1[1] += 1
				elif pygame.K_RIGHT in keys:
					dir1 = [1, 0]
					if empty(p1[0]+1, p1[1]): p1[0] += 1
				elif pygame.K_LEFT in keys:
					dir1 = [-1, 0]
					if empty(p1[0]-1, p1[1]): p1[0] -= 1
			
			steps += 1
			if steps % steps_to_alter_maze == 0:
				alterMaze()
			
			t_prev = t_curr
			
		else:
			d1[0] = ((t_curr - t_prev) / t_anim) * p1[0] + ((t_anim - (t_curr - t_prev)) / t_anim) * pp1[0]
			d1[1] = ((t_curr - t_prev) / t_anim) * p1[1] + ((t_anim - (t_curr - t_prev)) / t_anim) * pp1[1]
			
			d2[0] = ((t_curr - t_prev) / t_anim) * p2[0] + ((t_anim - (t_curr - t_prev)) / t_anim) * pp2[0]
			d2[1] = ((t_curr - t_prev) / t_anim) * p2[1] + ((t_anim - (t_curr - t_prev)) / t_anim) * pp2[1]
			

		screen.fill((255, 255, 255))
		
		# Bot1 path
		if playBot1 and showBotPath1:
			for p in path1:
				pygame.gfxdraw.aacircle(screen, int(p[0] * wallsize + wallsize / 2 - 1), int(p[1] * wallsize + wallsize / 2 - 1), int(wallsize / 2 * 0.5), (200, 200, 200))
		# Bot2 path
		if playBot2 and showBotPath2:
			for p in path2:
				pygame.gfxdraw.aacircle(screen, int(p[0] * wallsize + wallsize / 2 - 1), int(p[1] * wallsize + wallsize / 2 - 1), int(wallsize / 2 * 0.5), (200, 200, 200))
		
		
		# Walls
		for y in xrange(len(m)):
			for x in xrange(len(m[0])):
				pos = getDrawPos(x, y)
				if filled(x, y):
					#pygame.draw.rect(screen, (0, 0, 0), pos)
					drawBuilding(x, y)
				else:
					drawAsfalto(x, y)
		
		# Players
		#pygame.gfxdraw.aacircle(screen, int(d1[0] * wallsize + wallsize / 2 - 1), int(d1[1] * wallsize + wallsize / 2 - 1), int(wallsize / 2 * 0.8), (255,0,0))
		#pygame.gfxdraw.aacircle(screen, int(d2[0] * wallsize + wallsize / 2 - 1), int(d2[1] * wallsize + wallsize / 2 - 1), int(wallsize / 2 * 0.8), (0,0,255))
		#pygame.draw.circle(screen, (255,0,0), (int(d1[0] * wallsize + wallsize / 2 - 1), int(d1[1] * wallsize + wallsize / 2 - 1)), int(wallsize / 2 * 0.8))
		#pygame.draw.circle(screen, (0,0,255), (int(d2[0] * wallsize + wallsize / 2 - 1), int(d2[1] * wallsize + wallsize / 2 - 1)), int(wallsize / 2 * 0.8))
		
		p1_pos = (int(d1[0] * wallsize), int(d1[1] * wallsize))
		p2_pos = (int(d2[0] * wallsize), int(d2[1] * wallsize))
		
		rotated_player_1 = pygame.transform.rotate(player_1, angleFromDir(dir1))
		rotated_player_2 = pygame.transform.rotate(player_2, angleFromDir(dir2))
		
		screen.blit(rotated_player_1, (p1_pos[0], p1_pos[1], asfalto_size[0], asfalto_size[1]))
		screen.blit(rotated_player_2, (p2_pos[0], p2_pos[1], asfalto_size[0], asfalto_size[1]))
		
		pygame.display.flip()
		if dist(p1, p2) <= 1:
			break # Winning condition
	levelIndex = (levelIndex + 1) % len(levelFiles)
