# coding: latin-1

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
	
	if ini == end: return [ini]
	
	q = [ini]
	used = set(ini)
	pre = {}
	i = 0
	while len(q) - i > 0:
		c = q[i]
		ns = []
		if subte(c[0], c[1]):
			for y in xrange(len(m)):
				for x in xrange(len(m[0])):
					if (x, y) == (c[0], c[1]): continue
					ns.append((x, y))
		else:
			for j in xrange(4):
				ns.append((c[0] + dx[j], c[1] + dy[j]))
		
		for n in ns:
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
	global p1, p2, m, images, ob, casa
	
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
		plaza_3,
	]
	m = [line for line in maze.split("\n") if line.strip() != ""]
	print "-" * len(m[0])
	for y in xrange(len(m)):
		x1 = m[y].find("1")
		x2 = m[y].find("2")
		xo = m[y].find(".")
		xcasa = m[y].find("c")
		if x1 >= 0: p1 = [x1, y]
		if x2 >= 0: p2 = [x2, y]
		if xo >= 0: ob = [xo, y]
		if xcasa >= 0: casa = [xcasa, y]
		m[y] = m[y].replace("1", " ")
		m[y] = m[y].replace("2", " ")
		m[y] = m[y].replace(".", "O")
		m[y] = m[y].replace("c", "O")
		images.append([random.choice(imagePool) for x in xrange(len(m[0]))])

		print "".join(m[y])
	print "-" * len(m[0])
	print "Dimensions:", (len(m[0]), len(m))
	print "Players:", p1, p2
	m = [[c for c in row] for row in m]

def loadLevel(levelFile):
	global maze, dx, dy, p1, p2, dir1, dir2, cars_count
	print "Loading " + levelFile
	with open(levelFile) as f:
		data = f.read()
	data = data.split("\n\n")
	m = []
	loadMaze(data[0])
	if keepMoving:
		config = [line[:line.find("#")] for line in data[1].split("\n") if line[:line.find("#")].strip() != ""]
		#print config
		dir1 = [int(config[0].split(" ")[0]), int(config[0].split(" ")[1])]
		dir2 = [int(config[1].split(" ")[0]), int(config[1].split(" ")[1])]
		if len(config) > 2:
			cars_count = int(config[2].split(" ")[0])
		else:
			cars_count = 0
		print "Player directions:", dir1, dir2
	else:
		dx, dy = [0, 0, 1, -1], [1, -1, 0, 0]
		for i in xrange(4):
			if empty(p1[0]+dx[i], p1[1]+dy[i]): dir1 = [dx[i], dy[i]]
			if empty(p2[0]+dx[i], p2[1]+dy[i]): dir2 = [dx[i], dy[i]]
	

def empty(x, y):
	global m
	if x < 0 or y < 0 or x >= len(m[0]) or y >= len(m): return False
	return m[y][x] == " " or m[y][x] == "S"

def filled(x, y):
	global m
	if x < 0 or y < 0 or x >= len(m[0]) or y >= len(m): return False
	return m[y][x] == "X" or m[y][x] == "O" or m[y][x] == "S"

def subte(x, y):
	global m
	if x < 0 or y < 0 or x >= len(m[0]) or y >= len(m): return False
	return m[y][x] == "S"

def isMovable(c):
	if subte(c[0], c[1]): return False
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
		return
	
	for i in xrange(100):
		torem = 1 + int(random.random() * (len(m[0])-1)), 1 + int(random.random() * (len(m)-1)) # x, y
		if m[torem[1]][torem[0]] != "X": continue
		toadd = path[int(random.random() * len(path))]
		if dist(toadd, p1) == 0 or dist(toadd, p2) == 0: continue # VARIABLES DE CONFIG!!
		if list(p1) == list(toadd) or list(p2) == list(toadd): continue
		inCar = False
		for c in cars:
			if list(c) == list(toadd):
				inCar = True
				break
		if inCar: continue
		
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
	if ob and list((x, y)) == list(ob):
		img, img_size = obelisco, asfalto_size
	elif casa and list((x, y)) == list(casa):
		img, img_size = casa_rosada, asfalto_size
	else:
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
	if dir[0] == 0 and dir[1] == -1: return -90
	if dir[0] == -1 and dir[1] == 0: return 0
	return 0

def getScreenResolution():
	try:
		import gtk
		window = gtk.Window()
		screen = window.get_screen()
		monitors = []
		nmons = screen.get_n_monitors()
		for m in range(nmons): mg = screen.get_monitor_geometry(m)
		monitors.append(mg)
		curmon = screen.get_monitor_at_window(screen.get_active_window())
		x, y, width, height = monitors[curmon]
		return (width,height)
	except:
		try:
			import ctypes
			user32 = ctypes.windll.user32
			return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
		except:
			pass
	return 1024, 768

def changeDisplayMode(size):
	os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((SCREEN_RESOLUTION[0] - size[0]) / 2, (SCREEN_RESOLUTION[1] - size[1]) / 2)
	return pygame.display.set_mode(size)

def getRight(p, d, enSubte):
	if enSubte and subte(p[0], p[1]):
		for y in xrange(len(m)):
			for x in xrange(len(m[0])):
				if (x, y) == (p[0], p[1]): continue
				if subte(x, y):
					#print "Right subway", x, y
					return [x, y]
					
	dx, dy = [0, 0, -1, 1], [1, -1, 0, 0]
	ps = []
	for i in xrange(4):
		if d != [-dx[i], -dy[i]] and empty(p[0]+dx[i], p[1]+dy[i]): ps.append([p[0]+dx[i], p[1]+dy[i]])
	if len(ps) == 1: return ps[0]
	if d == [0, 1]: n = [-1, 0]
	if d == [0, -1]: n = [1, 0]
	if d == [1, 0]: n = [0, 1]
	if d == [-1, 0]: n = [0, -1]
	if empty(p[0]+n[0], p[1]+n[1]): return [p[0]+n[0], p[1]+n[1]]
	if empty(p[0]+d[0], p[1]+d[1]): return [p[0]+d[0], p[1]+d[1]]
	return [p[0]-d[0], p[1]-d[1]]

def getLeft(p, d, enSubte):
	if enSubte and subte(p[0], p[1]):
		for y in xrange(len(m)):
			for x in xrange(len(m[0])):
				if (x, y) == (p[0], p[1]): continue
				if subte(x, y):
					#print "Left subway", x, y
					return [x, y]
	
	dx, dy = [0, 0, -1, 1], [1, -1, 0, 0]
	ps = []
	for i in xrange(4):
		if d != [-dx[i], -dy[i]] and empty(p[0]+dx[i], p[1]+dy[i]): ps.append([p[0]+dx[i], p[1]+dy[i]])
	if len(ps) == 1: return ps[0]
	if d == [0, 1]: n = [1, 0]
	if d == [0, -1]: n = [-1, 0]
	if d == [1, 0]: n = [0, -1]
	if d == [-1, 0]: n = [0, 1]
	if empty(p[0]+n[0], p[1]+n[1]): return [p[0]+n[0], p[1]+n[1]]
	if empty(p[0]+d[0], p[1]+d[1]): return [p[0]+d[0], p[1]+d[1]]
	return [p[0]-d[0], p[1]-d[1]]

def getRandomDir(p, d, enSubte):
	opts = [getLeft(p, d, enSubte), getRight(p, d, enSubte)]
	return random.choice(opts)

def getRandomEmpty():
	while True:
		y = int(random.random() * len(m))
		x = int(random.random() * len(m[0]))
		if empty(x, y): return [x, y]

GAME_TITLE = "We Maze!"

SCREEN_RESOLUTION = getScreenResolution()

keepMoving = True
# TODO: Hacer bots para keepMoving!

imagesPath = "images/"
audioPath = "audio/"
fontsPath = "fonts/"
levelsPath = "levels/"
if keepMoving: levelsPath += "keep-moving/"
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


p1 = None
p2 = None
ob = None
casa = None
dir1 = [1, 0]
dir2 = [1, 0]
dirc = []
images = []

t_anim = 0.2
steps_to_alter_maze = 5

playBot1 = False
playBot2 = False
showBotPath1 = False
showBotPath2 = False



pygame.init()

pygame.display.set_caption(GAME_TITLE)

pygame.mixer.init()

# TODO: Repeat when finished!
#streetSound = pygame.mixer.Sound(audioPath + 'street_1.ogg')
streetSound = pygame.mixer.Sound(audioPath + 'street_3.ogg')
streetSound.set_volume(0.3)
streetSound.play(-1)

# La intro sólo se muestra si se abre la secuencia entera de niveles
introEnabled = (len(levelFiles) > 1)

if introEnabled:
	# TODO: Enseñarle a Manu arrays

	# Countdown

	screen = changeDisplayMode((640,480))
	font = pygame.font.Font(fontsPath + "countdown.ttf", 150)

	black = (0,0,0)
	text1 = font.render("Ready", 1, (255,0,0))
	text2 = font.render("Steady", 1, (255,0,0))
	text3 = font.render("Relax", 1, (255,0,0))
	pygame.mixer.music.load(audioPath + 'countdown.ogg')

	screen.fill(black)
	pygame.mixer.music.play(0)
	pygame.time.delay(100)
	screen.blit(text1, (130,150))
	pygame.display.flip()
	pygame.time.delay(1000)

	screen.fill(black)
	pygame.mixer.music.play(0)
	pygame.time.delay(100)
	screen.blit(text2, (80,150))
	pygame.display.flip()
	pygame.time.delay(1000)

	screen.fill(black)
	pygame.mixer.music.play(0)
	pygame.time.delay(100)
	screen.blit(text3, (130,150))
	pygame.display.flip()
	pygame.time.delay(2500)


# Loading background music

# TODO: Considerar si tenemos este problema, con esta solución:
# http://stackoverflow.com/a/13361935/1112654
pygame.mixer.music.load(audioPath + 'back.ogg')
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)



steps = 0

levelIndex = 0

while True:
	ob = None
	casa = None
	wallsize = 32
	
	cars_images = [loadImage("auto_rojo.png"), loadImage("auto_gris.png")]
	
	
	player_1 = loadImage("player_red.png")
	player_2 = loadImage("player_blue.png")
	
	asfalto_linea = loadImage("asfalto_linea.png")
	asfalto_esquina = loadImage("asfalto_esquina.png")
	asfalto_cruz = loadImage("asfalto_cruz.png")
	asfalto_t = loadImage("asfalto_t.png")
	asfalto_fin = loadImage("asfalto_fin.png")
	
	asfalto_size = asfalto_linea.get_size()
	
	obelisco = loadImage("obelisco.png")
	casa_rosada = loadImage("rosada.png")
	edificio_1 = loadImage("edificio_1.png")
	edificio_2 = loadImage("edificio_2.png")
	edificio_3 = loadImage("edificio_3.png")
	edificio_4 = loadImage("edificio_4.png")
	edificio_5 = loadImage("edificio_5.png")
	edificio_6 = loadImage("edificio_6.png")
	plaza = loadImage("plaza.png")
	plaza_3 = loadImage("plaza_3.png")
	
	subte_image = loadImage("subte.png")
	cars_count = 0
	levelFile = levelsPath + levelFiles[levelIndex]
	loadLevel(levelFile)
	print "Cars count:", cars_count
	
	cars_images = [random.choice(cars_images) for i in xrange(cars_count)]
	cars = [getRandomEmpty() for i in xrange(cars_count)]
	
	dirc = [random.choice([[0,1],[0,-1],[1,0],[-1,0]]) for i in xrange(cars_count)]
	
	size = width, height = wallsize * len(m[0]), wallsize * len(m)
	print "Screen size:", size
	
	pygame.display.set_caption(GAME_TITLE + " - %d: %s" % (levelIndex + 1, levelFile))
	screen = changeDisplayMode(size)
	keys = set()

	d1 = p1[:]
	d2 = p2[:]
	dc = [c[:] for c in cars]
	
	pp1 = p1[:]
	pp2 = p2[:]
	ppc = [c[:] for c in cars]
	
	pangle1 = angleFromDir(dir1)
	pangle2 = angleFromDir(dir2)
	panglec = [angleFromDir(d) for d in dirc]
	
	t_prev = time.time()
	path1 = []
	path2 = []
	won = False
	collision = False
	enSubte1 = False
	enSubte2 = False
	
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
			if won: break
			
			pp1 = p1[:]
			pp2 = p2[:]
			ppc = [c[:] for c in cars]
			pangle1 = angleFromDir(dir1)
			pangle2 = angleFromDir(dir2)
			panglec = [angleFromDir(d) for d in dirc]
			
			if playBot1: path1 = bfs_p1_to_p2()
			if playBot2: path2 = bfs_p2_to_p1()
			
			#==========================
			# Controllers
			#==========================
			
			
			# Subte P1
			if not enSubte1 and subte(pp1[0], pp1[1]):
				enSubte1 = True
			else:
				enSubte1 = False
			#print "Subway1", enSubte1
			
			
			# Bot 1
			if playBot1:
				next_p1 = list(path1[0])
				if next_p1 != p1: dir1 = [next_p1[0] - p1[0], next_p1[1] - p1[1]]
				p1 = next_p1
			else:
				# Player 1 - Always moving
				if keepMoving:
					next_p1 = getLeft(p1, dir1, enSubte1) if pygame.K_LEFT in keys else getRight(p1, dir1, enSubte1)
					if not enSubte1 and next_p1 != p1: dir1 = [next_p1[0] - p1[0], next_p1[1] - p1[1]]
					p1 = next_p1
				
				# Player 1 - Keys
				else:
					if pygame.K_UP in keys:
						if empty(p1[0], p1[1]-1):
							dir1 = [0, -1]
							p1[1] -= 1
					elif pygame.K_DOWN in keys:
						if empty(p1[0], p1[1]+1):
							dir1 = [0, 1]
							p1[1] += 1
					elif pygame.K_RIGHT in keys:
						if empty(p1[0]+1, p1[1]):
							dir1 = [1, 0]
							p1[0] += 1
					elif pygame.K_LEFT in keys:
						if empty(p1[0]-1, p1[1]):
							dir1 = [-1, 0]
							p1[0] -= 1
			
			# Subte P2
			if not enSubte2 and subte(pp2[0], pp2[1]):
				enSubte2 = True
			else:
				enSubte2 = False
			#print "Subway2", enSubte2
			
			# Bot 2
			if playBot2:
				next_p2 = list(path2[0])
				if not enSubte2 and next_p2 != p2: dir2 = [next_p2[0] - p2[0], next_p2[1] - p2[1]]
				p2 = next_p2
			else:
				# Player 2 - Always moving
				if keepMoving:
					next_p2 = getRight(p2, dir2, enSubte2) if pygame.K_RIGHT in keys else getLeft(p2, dir2, enSubte2)
					if not enSubte2 and next_p2 != p2: dir2 = [next_p2[0] - p2[0], next_p2[1] - p2[1]]
					p2 = next_p2
				else:
					# Player 2 - Keys
					if pygame.K_w in keys:
						if empty(p2[0], p2[1]-1):
							dir2 = [0, -1]
							p2[1] -= 1
					elif pygame.K_s in keys:
						if empty(p2[0], p2[1]+1):
							dir2 = [0, 1]
							p2[1] += 1
					elif pygame.K_d in keys:
						if empty(p2[0]+1, p2[1]):
							dir2 = [1, 0]
							p2[0] += 1
					elif pygame.K_a in keys:
						if empty(p2[0]-1, p2[1]):
							dir2 = [-1, 0]
							p2[0] -= 1
			
			for i in xrange(len(cars)):
				c = cars[i]
				next_c = getRandomDir(c, dirc[i], False)
				if next_c != c: dirc[i] = [next_c[0] - c[0], next_c[1] - c[1]]
				cars[i] = next_c
			
			if not enSubte1:
				if abs(pangle1 + 360 - angleFromDir(dir1)) < abs(pangle1 - angleFromDir(dir1)): pangle1 += 360
				elif abs(pangle1 - 360 - angleFromDir(dir1)) < abs(pangle1 - angleFromDir(dir1)): pangle1 -= 360
			if not enSubte2:
				if abs(pangle2 + 360 - angleFromDir(dir2)) < abs(pangle2 - angleFromDir(dir2)): pangle2 += 360
				elif abs(pangle2 - 360 - angleFromDir(dir2)) < abs(pangle2 - angleFromDir(dir2)): pangle2 -= 360
			
			for i in xrange(len(cars)):
				pangle = panglec[i]
				if abs(pangle + 360 - angleFromDir(dirc[i])) < abs(pangle - angleFromDir(dirc[i])): panglec[i] += 360
				elif abs(pangle2 - 360 - angleFromDir(dirc[i])) < abs(pangle - angleFromDir(dirc[i])): panglec[i] -= 360
			
			steps += 1
			if steps % steps_to_alter_maze == 0:
				alterMaze()
			
			collision = (dist(p1, p2) == 1 and dir1 == [-dir2[0], -dir2[1]] and list(p2) == [p1[0]-dir1[0], p1[1]-dir1[1]] and list(p1) == [p2[0]-dir2[0], p2[1]-dir2[1]])
			if dist(p1, p2) == 0 or collision:
				won = True
			
			t_prev = t_curr
			
		else:
			if not enSubte1:
				d1[0] = ((t_curr - t_prev) / t_anim) * p1[0] + ((t_anim - (t_curr - t_prev)) / t_anim) * pp1[0]
				d1[1] = ((t_curr - t_prev) / t_anim) * p1[1] + ((t_anim - (t_curr - t_prev)) / t_anim) * pp1[1]
				if won and collision: d1 = [(d1[0]+pp1[0])/2., (d1[1]+pp1[1])/2.]
				if abs(pangle1 - angleFromDir(dir1)) < 180:
					p1_ang = ((t_curr - t_prev) / t_anim) * angleFromDir(dir1) + ((t_anim - (t_curr - t_prev)) / t_anim) * pangle1
				else:
					p1_ang = angleFromDir(dir1)
			
			if not enSubte2:
				d2[0] = ((t_curr - t_prev) / t_anim) * p2[0] + ((t_anim - (t_curr - t_prev)) / t_anim) * pp2[0]
				d2[1] = ((t_curr - t_prev) / t_anim) * p2[1] + ((t_anim - (t_curr - t_prev)) / t_anim) * pp2[1]
				if won and collision: d2 = [(d2[0]+pp2[0])/2., (d2[1]+pp2[1])/2.]
				if abs(pangle2 - angleFromDir(dir2)) < 180:
					p2_ang = ((t_curr - t_prev) / t_anim) * angleFromDir(dir2) + ((t_anim - (t_curr - t_prev)) / t_anim) * pangle2
				else:
					p2_ang = angleFromDir(dir2)
			c_ang = [0.0 for c in cars]
			for i in xrange(len(cars)):
				c = cars[i]
				
				dc[i][0] = ((t_curr - t_prev) / t_anim) * c[0] + ((t_anim - (t_curr - t_prev)) / t_anim) * ppc[i][0]
				dc[i][1] = ((t_curr - t_prev) / t_anim) * c[1] + ((t_anim - (t_curr - t_prev)) / t_anim) * ppc[i][1]
				if won and collision: dc[i] = [(dc[i][0]+ppc[i][0])/2., (dc[i][1]+ppc[i][1])/2.]
				if abs(panglec[i] - angleFromDir(dirc[i])) < 180:
					c_ang[i] = ((t_curr - t_prev) / t_anim) * angleFromDir(dirc[i]) + ((t_anim - (t_curr - t_prev)) / t_anim) * panglec[i]
				else:
					c_ang[i] = angleFromDir(dirc[i])

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
				if m[y][x] == 'X' or m[y][x] == 'O':
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
		
		rotated_player_1 = pygame.transform.rotate(player_1, p1_ang)
		rotated_player_2 = pygame.transform.rotate(player_2, p2_ang)
		
		screen.blit(rotated_player_1, (p1_pos[0], p1_pos[1], asfalto_size[0], asfalto_size[1]))
		screen.blit(rotated_player_2, (p2_pos[0], p2_pos[1], asfalto_size[0], asfalto_size[1]))
		
		# Subway
		for y in xrange(len(m)):
			for x in xrange(len(m[0])):
				pos = getDrawPos(x, y)
				if subte(x, y):
					#subte_pos = (int(x * wallsize), int(y * wallsize))
					screen.blit(subte_image, (pos[0], pos[1], asfalto_size[0], asfalto_size[1]))
					#pygame.draw.rect(screen, (255, 0, 0), pos)
		
		# Cars
		for ci in xrange(len(cars)):
			c = cars[ci]
			c_pos = (int(dc[ci][0] * wallsize), int(dc[ci][1] * wallsize))
			rotated_c = pygame.transform.rotate(cars_images[ci], c_ang[ci])
			screen.blit(rotated_c, (c_pos[0], c_pos[1], asfalto_size[0], asfalto_size[1]))
		
		pygame.display.flip()
		
	levelIndex += 1
	if levelIndex == len(levelFiles):
		if len(levelFiles) > 1: break
		else: levelIndex = 0

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				sys.exit()
	#screen.fill((255, 255, 255))
	screen = changeDisplayMode((640,480))
	screen.fill((0, 0, 0))
	#Write credits here
	pygame.mixer.music.stop
	pygame.mixer.music.load(audioPath + 'credits.ogg')
	pygame.mixer.music.play(-1)
	myfont = pygame.font.SysFont("Verdana", 24)
	label = myfont.render("We finally met dude! :D", 1, (255, 255, 255))
	screen.blit(label, (170, 50))
	label = myfont.render("Credits:", 1, (255, 255, 255))
	screen.blit(label, (100, 200))
	label = myfont.render("Main Programmer: Axel Brzostowski", 1, (255, 255, 255))
	screen.blit(label, (100, 250))
	label = myfont.render("Level Designer: Blas Ingiulla", 1, (255, 255, 255))
	screen.blit(label, (100, 280))
	label = myfont.render("Music: Leandro Bordino", 1, (255, 255, 255))
	screen.blit(label, (100, 340))
	label = myfont.render("Music: Salazar Riquelme Federico Agustin", 1, (255, 255, 255))
	screen.blit(label, (100, 370))
	label = myfont.render("Junior Programmer: Manuel Parma", 1, (255, 255, 255))
	screen.blit(label, (100, 310))
	label = myfont.render("Artists: Everyone", 1, (255, 255, 255))
	screen.blit(label, (100, 400))
	pygame.display.flip()

