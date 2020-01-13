import pygame, json, algorithms, random, math
from config import Config


class Tile(pygame.Rect):
	tilesDict = {} # id to tile
	coordToIdDict = {} # coord to id
	neighborsDict = {} # id to neighbors ids
	counter = 1 # to keep track of the total number of the tiles
	Adj = {} # adjacency list that represents the map

	pathToTargetList = [] # list of nodes to reach target from source
	idToCoordDict = {} # to draw frontier when showing exploration
	levelToIdList = [] # used to update the frontier when showing exploration
	currentFrontier = [] # used to draw the frontier when showing exploration

	idToLevelDict = {} # id to level
	idToCostDict = {} # for Dijkstra, Best-First Search and A*
	levelToCostList = []
	idToCostAux = {} # to display tile cost during exploration

	blockedTiles = [] # list of blocked tiles
	explored_tiles = [] # list of explored tiles. Used to remove dark mask from explored tiles

	def __init__(self, x, y, TILE_W, TILE_H):
		pygame.Rect.__init__(self, x, y, TILE_W, TILE_H)
		self.id = str(Tile.counter)
		Tile.counter += 1 # increase total tile counter

		self.coord = (x//Config.TILE_SIZE, y//Config.TILE_SIZE)
		self.width = TILE_W
		self.height = TILE_H

		Tile.tilesDict[self.id] = self # map this id to this tile
		Tile.coordToIdDict[self.coord] = self.id # map this coord to this id
		Tile.idToCoordDict[self.id] = (self.x, self.y)

		self.walkable = True
		if self.id in Tile.blockedTiles:
			self.walkable = False

		self.W = random.randint(1,3) # default cost for Dijkstra

	def draw_tile(self, screen):
		# draw tiles
		x = self.x + Config.PADDING
		y = self.y + Config.PADDING + Config.margin_top

		# draw walkable / blocked
		if self.walkable:
			if self.W == 1 or Config.currentAlgorithm in ["BFS", "DFS"]:
				screen.blit(Image.tileWalkable1Image, (x, y))
			elif self.W == 2:
				screen.blit(Image.tileWalkable2Image, (x, y))
			elif self.W == 3:
				screen.blit(Image.tileWalkable3Image, (x, y))
		else:
			screen.blit(Image.tileBlockedImage, (x, y))

		# add dark mask if not explored
		if self.id not in Tile.explored_tiles and self.walkable:
			screen.blit(Image.tileUnvisitedImage, (x, y))

		# draw source and target
		if self.id == Config.source:
			screen.blit(Image.tileSourceImage, (x, y))
		elif self.id == Config.target:
			screen.blit(Image.tileTargetImage, (x, y))

		# if showing exploration, draw current frontier
		if GameController.isShowingExploration:
			for frontierTileId in Tile.currentFrontier:
				frontierPos = Tile.idToCoordDict[frontierTileId]
				x = frontierPos[0]+Config.PADDING
				y = frontierPos[1]+Config.PADDING+Config.margin_top
				screen.blit(Image.frontierImage, (x, y))

	def draw_text(self, screen):
		x = self.x + Config.PADDING
		y = self.y + Config.PADDING + Config.margin_top

		if self.walkable:
			# print level
			if Config.currentAlgorithm=="BFS" or Config.currentAlgorithm=="DFS":
				dictToDisplay = Tile.idToLevelDict

			elif Config.currentAlgorithm=="Dijkstra" or Config.currentAlgorithm=="B_FS" or Config.currentAlgorithm=="A*":
				dictToDisplay = Tile.idToCostAux
				# print tile W for debug
				# cost_text = Font.fontId.render(str(self.W), True, Color.white)
				# screen.blit(cost_text, (x+2, y+2))

			if self.id in dictToDisplay.keys():
				level_text = Font.fontLevel.render(str(dictToDisplay[self.id]), True, Color.white)
				screen.blit(level_text, (x + Config.TILE_SIZE//2 - 6, y + Config.TILE_SIZE//2 - 5)) # center of the tile

			# display id for debug
			# id_text = Font.fontId.render(str(self.id), True, Color.white)
			# screen.blit(id_text, (x+2, y+Config.TILE_SIZE-10))

	def draw_shortest_path(self, screen):
		if not Tile.pathToTargetList:
			return

		if self.id in Tile.pathToTargetList:
			aux = (self.x+Config.PADDING, self.y+Config.PADDING+Config.margin_top)
			screen.blit(Image.shortestPathImage, aux)

	@staticmethod
	def build_neighbors_dict():
		for tile in Tile.tilesDict.values():
			if not tile.walkable: # skip tile if not walkable
				continue
			x = tile.coord[0]
			y = tile.coord[1]
			neighborsList = []

			# print("\nTile %s " % tile.id)
			neighborCoord = (x, y-1) # above
			if ( neighborCoord in Tile.coordToIdDict.keys() ):
				if (Tile.tilesDict[Tile.coordToIdDict[neighborCoord]].walkable):
					neighborsList.append(Tile.coordToIdDict[neighborCoord])
					# print("\thas neighbor above " + str(neighborCoord))

			neighborCoord = (x+1, y) # right
			if ( neighborCoord in Tile.coordToIdDict.keys() ):
				if (Tile.tilesDict[Tile.coordToIdDict[neighborCoord]].walkable):
					neighborsList.append(Tile.coordToIdDict[neighborCoord])
					# print("\thas neighbor right " + str(neighborCoord))

			neighborCoord = (x, y+1) # below
			if ( neighborCoord in Tile.coordToIdDict.keys() ):
				if (Tile.tilesDict[Tile.coordToIdDict[neighborCoord]].walkable):
					neighborsList.append(Tile.coordToIdDict[neighborCoord])
					# print("\thas neighbor below " + str(neighborCoord))

			neighborCoord = (x-1, y) # left
			if ( neighborCoord in Tile.coordToIdDict.keys() ):
				if (Tile.tilesDict[Tile.coordToIdDict[neighborCoord]].walkable):
					neighborsList.append(Tile.coordToIdDict[neighborCoord])
					# print("\thas neighbor left " + str(neighborCoord))

			Tile.neighborsDict[tile.id] = neighborsList # map tile id to neighbor id


class GameController:
	ticksLastFrame = 0
	isShowingExploration = False
	currentLevelExplored = 0
	mapData = {} # map data to save
	currentAlg = None

	@staticmethod
	def execute_current_algorithm():
		Adj, source, target = Tile.neighborsDict, Config.source, Config.target

		W = {} # weight dictionary that maps each tile to its cost
		for tile in Tile.tilesDict.values():
			W[tile.id] = tile.W

		algDict = {
			"BFS" : algorithms.BFS(Adj, source, target),
			"DFS" : algorithms.DFS(Adj, source, target),
			"Dijkstra" : algorithms.Dijkstra(Adj, W, source, target),
			"B_FS" : algorithms.B_FS(Adj, W, source, target),
			"A*" : algorithms.A_star(Adj, W, source, target),
		}

		alg = algDict[Config.currentAlgorithm]
		if Config.currentAlgorithm in ["BFS", "DFS"]:
			Tile.pathToTargetList, Tile.idToLevelDict, Tile.levelToIdList = alg.search()
			Tile.explored_tiles = Tile.idToLevelDict.keys() # to draw explored tiles

		elif Config.currentAlgorithm in ["Dijkstra", "B_FS", "A*"]:
			Tile.pathToTargetList, Tile.idToCostDict, Tile.levelToIdList, Tile.explored_tiles, Tile.levelToCostList = alg.search()
			Tile.idToCostAux = Tile.idToCostDict
		GameController.currentAlg = alg

	@staticmethod
	def set_target_source(click):
		(m_x, m_y) = GameController._get_clicked_tile()

		if (m_x, m_y) in Tile.coordToIdDict.keys():
			tile_id_clicked = Tile.coordToIdDict[(m_x, m_y)]

			if click == 1 and tile_id_clicked != Config.source: # left click and tile clicked is not source
				if tile_id_clicked == Config.target and Config.currentAlgorithm in ["BFS","DFS","Dijkstra"]:
					Config.target = None
				else:
					Config.target = tile_id_clicked

			elif click == 3 and tile_id_clicked != Config.target: # right click and tile clicked is not target
				# avoid to put source on blocked tile
				if Tile.tilesDict[tile_id_clicked].walkable:
					Config.source = tile_id_clicked
			else:
				print("bean/GameController/set_target_source: cannot place source/target")

			# update shortest path
			GameController.execute_current_algorithm()

	@staticmethod
	def set_walkable(click):
		(m_x, m_y) = GameController._get_clicked_tile()

		if click == 1: # left click
			isWalkable = False
		elif click == 3: # right click
			isWalkable = True
		else:
			return

		if (m_x, m_y) in Tile.coordToIdDict.keys():
			tile_id = Tile.coordToIdDict[(m_x, m_y)]
			Tile.tilesDict[tile_id].walkable = isWalkable

			if tile_id in Tile.blockedTiles and isWalkable: # remove tile from blockedTiles
				Tile.blockedTiles.remove(tile_id)
			elif tile_id not in Tile.blockedTiles and not isWalkable: # add tile to blockedTiles
				Tile.blockedTiles.append(tile_id)

			Tile.build_neighbors_dict() # re-build adjacency list
			GameController.execute_current_algorithm()

	@staticmethod
	def edit_tile_cost(click):
		(m_x, m_y) = GameController._get_clicked_tile()

		if (m_x, m_y) in Tile.coordToIdDict.keys():
			tile_id_clicked = Tile.coordToIdDict[(m_x, m_y)]

			if click == 1:
				dW = 1
			elif click == 3:
				dW = -1

			Tile.tilesDict[tile_id_clicked].W += dW

			if Tile.tilesDict[tile_id_clicked].W < 1:
				Tile.tilesDict[tile_id_clicked].W = 1

			# update shortest path
			GameController.execute_current_algorithm()

	@staticmethod
	def show_exploration():
		t = pygame.time.get_ticks()
		dt = (t - GameController.ticksLastFrame)

		if dt >= Config.showExplorationDelay:

			# update explored tiles
			Tile.currentFrontier = Tile.levelToIdList[GameController.currentLevelExplored]

			# add current frontier to explored tiles
			for new_tile in Tile.currentFrontier:
				Tile.explored_tiles.append(new_tile)

			# if Dijkstra, update tile cost
			if Config.currentAlgorithm=="Dijkstra" or Config.currentAlgorithm=="B_FS" or Config.currentAlgorithm=="A*":
				currentTile = Tile.levelToIdList[GameController.currentLevelExplored]
				currentTile = currentTile[0]
				Tile.idToCostAux[currentTile] = Tile.levelToCostList[GameController.currentLevelExplored]

			# show_exploration finish
			if GameController.currentLevelExplored == len(Tile.levelToIdList)-1:
				Tile.pathToTargetList = GameController.currentAlg.find_path() # show path at the end of exploration

				print("exploration finished")
				GameController.isShowingExploration = False

			GameController.currentLevelExplored += 1
			GameController.ticksLastFrame = t

	@staticmethod
	def saveMap():

		idToWDict = {}
		for tile in Tile.tilesDict.values():
			idToWDict[tile.id] = tile.W

		GameController.mapData = {"target":Config.target, "source":Config.source, "blocked_tiles":Tile.blockedTiles, "tile_w":idToWDict}
		with open('map.json', 'w') as f:
		    json.dump(GameController.mapData, f)
		print("map saved to file")

	@staticmethod
	def switch_alg(click):
		algIdx = Config.algList.index(Config.currentAlgorithm)

		if click == 1 and algIdx < len(Config.algList)-1:
			algIdx += 1

		elif click == 3 and algIdx > 0:
			algIdx -= 1

		Config.currentAlgorithm = Config.algList[algIdx]
		print("current algorithm: %s" % Config.currentAlgorithm)

		if Config.currentAlgorithm in ["B_FS", "A*"] and Config.target==None:
			GameController.set_random_target() # informed search needs a target
		GameController.execute_current_algorithm()

	@staticmethod
	def load_map():
		with open('map.json', 'r') as f:
			GameController.mapData = json.load(f)
			Config.source = GameController.mapData["source"]
			Config.target = GameController.mapData["target"]
			Tile.blockedTiles = GameController.mapData["blocked_tiles"]
			idToWDict = GameController.mapData["tile_w"]

		for tile in Tile.tilesDict.values():
			if tile.id in Tile.blockedTiles:
				tile.walkable = False
			tile.W = idToWDict[tile.id]
			# print("tile %s has W %f" % (tile.id, tile.W))

		print("map loaded from file")

	@staticmethod
	def _get_clicked_tile():
		m_pos = pygame.mouse.get_pos()
		m_x = (m_pos[0] - Config.PADDING) // Config.TILE_SIZE
		m_y = (m_pos[1] - Config.PADDING - Config.margin_top) // Config.TILE_SIZE
		return (m_x, m_y)

	@staticmethod
	def set_random_target():
		# this is used when the current algorithm is uninformed search and target is None,
		# and the algorithm is switched to informed search, which needs a target
		for tile in Tile.tilesDict.values():
			if tile.walkable and tile.id != Config.source:
				Config.target = tile.id
				return


class Button:
	buttonDict = {}

	def __init__(self, x, y, w, h, text=None, action=None):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.text = text
		self.action = action

		rect = pygame.Rect((x, y), (w, h))
		self.rect = rect

		if action=="set_target_source":
			self.active = True
		else:
			self.active = False

		Button.buttonDict[self.action] = self # map button action to button

	def check_if_click(self, cursor, click):
		if self.rect.collidepoint(cursor):

			if self.action == "show_exploration":
				self.set_active()
				GameController.isShowingExploration = True

				# initialize GameController show_exploration() parameters
				Tile.explored_tiles = []
				GameController.currentLevelExplored = 0

				# initialize path to target to null
				Tile.pathToTargetList = []

				if Config.currentAlgorithm =="Dijkstra" or Config.currentAlgorithm =="B_FS" or Config.currentAlgorithm =="A*":
					# initialize all tiles cost to inf
					Tile.idToCostAux = {}
					for id in Tile.tilesDict.keys():
						Tile.idToCostAux[id] = math.inf

			elif self.action == "save_map":
				GameController.saveMap()

			elif self.action == "switch_alg":
				GameController.switch_alg(click)

				# update button text
				self.text = "Alg: " + Config.currentAlgorithm

	def set_active(self):
		# first deactivate all buttons
		for btn in Button.buttonDict.values():
			btn.active = False

		# then activate this button
		self.active = True

	def draw_button(self, screen):
		mouse = pygame.mouse.get_pos() # to check if mouse is hovering
		if (self.x < mouse[0] < self.x+self.w and self.y < mouse[1] < self.y+self.h) \
			or self.active:
			# draw highlighted button
			screen.fill(Color.button_ac, self.rect)
		else:
			screen.fill(Color.button_ic, self.rect)

		# draw_text
		textSurf, textRect = self.text_objects(self.text, Font.fontButton)
		textRect.center = (self.x + self.w/2, self.y + self.h/2)
		screen.blit(textSurf,textRect)

	def text_objects(self, text, font):
		textSurface = font.render(text, True, (0,0,0))
		return textSurface, textSurface.get_rect()


class Font:
	@staticmethod
	def set_font():
		Font.fontId = pygame.font.Font('freesansbold.ttf', 9)
		Font.fontLevel = pygame.font.Font('freesansbold.ttf', 13)
		Font.fontButton = pygame.font.Font('freesansbold.ttf', 15)


class Image:
	tileSourceImage = pygame.image.load("img/tile_source.png")
	tileTargetImage = pygame.image.load("img/tile_target.png")
	walkable1 = pygame.image.load("img/walkable1.jpg")
	walkable2 = pygame.image.load("img/walkable2.jpg")
	walkable3 = pygame.image.load("img/walkable3.jpg")
	tileBlockedImage = pygame.image.load("img/blocked.jpg")
	tileUnvisited = pygame.image.load("img/unvisited.png")
	shortestPathImage = pygame.image.load("img/shortest_path.png")
	frontierImage = pygame.image.load("img/frontier.png")
	backgroundImage = pygame.image.load("img/blocked.jpg")

	tileSourceImage = pygame.transform.scale(tileSourceImage, (Config.TILE_SIZE, Config.TILE_SIZE))
	tileTargetImage = pygame.transform.scale(tileTargetImage, (Config.TILE_SIZE, Config.TILE_SIZE))
	tileWalkable1Image = pygame.transform.scale(walkable1, (Config.TILE_SIZE, Config.TILE_SIZE))
	tileWalkable2Image = pygame.transform.scale(walkable2, (Config.TILE_SIZE, Config.TILE_SIZE))
	tileWalkable3Image = pygame.transform.scale(walkable3, (Config.TILE_SIZE, Config.TILE_SIZE))
	tileBlockedImage = pygame.transform.scale(tileBlockedImage, (Config.TILE_SIZE, Config.TILE_SIZE))
	tileUnvisitedImage = pygame.transform.scale(tileUnvisited, (Config.TILE_SIZE, Config.TILE_SIZE))
	frontierImage = pygame.transform.scale(frontierImage, (Config.TILE_SIZE, Config.TILE_SIZE))
	shortestPathImage = pygame.transform.scale(shortestPathImage, (Config.TILE_SIZE, Config.TILE_SIZE))
	backgroundImage = pygame.transform.scale(backgroundImage, (1920, 1080))


class Color:
	white = (255,255,255)
	black = (0,0,0)
	button_ic = (153, 76, 0)
	button_ac = (204, 102, 0)
