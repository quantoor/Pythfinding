
import pygame, json, algorithms
from math import *
from config import Config


class Tile(pygame.Rect):
	tilesDict = {} # id to tile
	coordToIdDict = {} # coord to id
	neighborsDict = {} # id to neighbors ids
	counter = 1 # to keep track of the total number of the tiles
	Adj = {} # adjacency list
	shortestPathList = [] # list of nodes to reach target from source
	idToLevelDict = {} # id to level
	levelToIdDict = {} # level to ids

	blocked_tiles = []
	explored_tiles = []

	def __init__(self, x, y, TILE_W, TILE_H):
		pygame.Rect.__init__(self, x, y, TILE_W, TILE_H)
		self.id = str(Tile.counter)
		Tile.counter += 1 # increase total tile counter
		# print("Created tile %s at pos (%d, %d)" % (self.id, x, y))

		self.coord = (x//Config.TILE_SIZE, y//Config.TILE_SIZE)
		self.width = TILE_W
		self.height = TILE_H

		Tile.tilesDict[self.id] = self # map this id to this tile
		Tile.coordToIdDict[self.coord] = self.id # map this coord to this id

		self.walkable = True
		if self.id in Tile.blocked_tiles:
			self.walkable = False

	def draw_tile(self, screen):
		# draw tiles
		x = self.x + Config.BORDER
		y = self.y + Config.BORDER

		if self.walkable:
			screen.blit(Image.tileWalkableImage, (x, y))
		else:
			screen.blit(Image.tileBlockedImage, (x, y))

		# add dark mask if not explored
		if self.id not in Tile.explored_tiles:
			screen.blit(Image.tileExploredImage, (x, y))

		# draw source and target
		if self.id == Config.source:
			screen.blit(Image.tileSourceImage, (x, y))
		elif self.id == Config.target:
			screen.blit(Image.tileTargetImage, (x, y))

	def draw_text(self, screen):
		id_text = Font.font12.render(str(self.id), True, (255, 255, 255))
		screen.blit(id_text, (self.x+Config.TILE_SIZE//2-5+Config.BORDER, self.y+Config.TILE_SIZE//2-5+Config.BORDER))

		# print level
		if (self.walkable) and self.id in Tile.idToLevelDict.keys():
			level_text = Font.font10.render(str(Tile.idToLevelDict[self.id]), True, (255, 255, 255))
			screen.blit(level_text, (self.x+Config.BORDER+2, self.y+Config.BORDER+2))

	def draw_shortest_path(self, screen):
		if not Tile.shortestPathList:
			return

		if self.id in Tile.shortestPathList:
			aux = (self.x+Config.BORDER, self.y+Config.BORDER)
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

	@staticmethod # TODO put together with set new source
	def setNewTarget():
		m_pos = pygame.mouse.get_pos()
		m_x = (m_pos[0] - Config.BORDER) // Config.TILE_SIZE
		m_y = (m_pos[1] - Config.BORDER) // Config.TILE_SIZE
		try:
			new_target_id = Tile.coordToIdDict[(m_x, m_y)]
			Config.target = new_target_id
			Tile.shortestPathList, Tile.idToLevelDict, Tile.levelToIdDict = algorithms.BFS(Tile.neighborsDict, Config.source, Config.target)
			Tile.explored_tiles = Tile.idToLevelDict.keys()
			print("(%d, %d) is the new target" % (m_x, m_y))
		except:
			pass

	@staticmethod
	def setNewSource():
		m_pos = pygame.mouse.get_pos()
		m_x = (m_pos[0] - Config.BORDER) // Config.TILE_SIZE
		m_y = (m_pos[1] - Config.BORDER) // Config.TILE_SIZE
		try:
			new_source_id = Tile.coordToIdDict[(m_x, m_y)]
			Config.source = new_source_id
			Tile.shortestPathList, Tile.idToLevelDict, Tile.levelToIdDict = algorithms.BFS(Tile.neighborsDict, Config.source, Config.target)
			Tile.explored_tiles = Tile.idToLevelDict.keys()
			print("(%d, %d) is the new source" % (m_x, m_y))
		except:
			pass

	@staticmethod
	def setWalkable(isWalkable):
		m_pos = pygame.mouse.get_pos()
		m_x = (m_pos[0] - Config.BORDER) // Config.TILE_SIZE
		m_y = (m_pos[1] - Config.BORDER) // Config.TILE_SIZE
		try:
			tile_id = Tile.coordToIdDict[(m_x, m_y)]
			Tile.tilesDict[tile_id].walkable = isWalkable

			if tile_id in Tile.blocked_tiles and isWalkable: # remove tile from blocked_tiles
				Tile.blocked_tiles.remove(tile_id)
			elif tile_id not in Tile.blocked_tiles and not isWalkable: # add tile to blocked_tiles
				print("added to blocked tiles")
				Tile.blocked_tiles.append(tile_id)

			Tile.build_neighbors_dict() # re-build adjacency list
			Tile.shortestPathList, Tile.idToLevelDict, Tile.levelToIdDict = algorithms.BFS(Tile.neighborsDict, Config.source, Config.target)
			Tile.explored_tiles = Tile.idToLevelDict.keys()
		except:
			pass

	@staticmethod
	def show_exploration():
		t = pygame.time.get_ticks()
		dt = (t - GameController.ticksLastFrame)

		if dt >= Config.showExplorationDelay:
			GameController.currentLevelExplored += 1
			GameController.ticksLastFrame = t

			# update explored tiles
			new_explored_tiles = Tile.levelToIdDict[GameController.currentLevelExplored]
			for new_tile in new_explored_tiles:
				Tile.explored_tiles.append(new_tile)

			# show_exploration finish
			if GameController.currentLevelExplored == max(Tile.levelToIdDict.keys()):
				print("exploration finished")
				GameController.isShowingExploration = False

	@staticmethod
	def saveMap():
		GameController.mapData = {"target":Config.target, "source":Config.source, "blocked_tiles":Tile.blocked_tiles}
		with open('map.json', 'w') as f:
		    json.dump(GameController.mapData, f)
		print("map saved to file")

	@staticmethod
	def load_map():
		with open('map.json', 'r') as f:
			GameController.mapData = json.load(f)
			Config.source = GameController.mapData["source"]
			Config.target = GameController.mapData["target"]
			Tile.blocked_tiles = GameController.mapData["blocked_tiles"]
			print("map loaded from file")


class Button():
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

	def check_if_click(self, cursor):
		if self.rect.collidepoint(cursor):
			self.set_active()
			print(self.action)

			if self.action == "show_exploration":
				GameController.isShowingExploration = True

				# initialize GameController show_exploration() parameters
				Tile.explored_tiles = []
				GameController.currentLevelExplored = 0

			elif self.action == "save_map":
				GameController.saveMap()

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
		textSurf, textRect = self.text_objects(self.text, Font.font15)
		textRect.center = (self.x + self.w/2, self.y + self.h/2)
		screen.blit(textSurf,textRect)

	def text_objects(self, text, font):
		textSurface = font.render(text,True,(0,0,0))
		return textSurface, textSurface.get_rect()


class Font:
	@staticmethod
	def set_font():
		Font.font10 = pygame.font.Font('freesansbold.ttf', 10)
		Font.font12 = pygame.font.Font('freesansbold.ttf', 12)
		Font.font15 = pygame.font.Font('freesansbold.ttf', 15)


class Image:
	tileSourceImage = pygame.image.load("img/tile_source.png")
	tileTargetImage = pygame.image.load("img/tile_target.png")
	tileWalkableImage = pygame.image.load("img/tile_walkable.png")
	tileBlockedImage = pygame.image.load("img/tile_blocked.png")
	tileExploredImage = pygame.image.load("img/tile_explored.png")
	shortestPathImage = pygame.image.load("img/shortest_path.png")

	tileSourceImage = pygame.transform.scale(tileSourceImage, (Config.TILE_SIZE, Config.TILE_SIZE))
	tileTargetImage = pygame.transform.scale(tileTargetImage, (Config.TILE_SIZE, Config.TILE_SIZE))
	tileWalkableImage = pygame.transform.scale(tileWalkableImage, (Config.TILE_SIZE, Config.TILE_SIZE))
	tileBlockedImage = pygame.transform.scale(tileBlockedImage, (Config.TILE_SIZE, Config.TILE_SIZE))
	tileExploredImage = pygame.transform.scale(tileExploredImage, (Config.TILE_SIZE, Config.TILE_SIZE))
	shortestPathImage = pygame.transform.scale(shortestPathImage, (Config.TILE_SIZE, Config.TILE_SIZE))


class Color:
	background = (255, 255, 102)
	white = (255,255,255)
	black = (0,0,0)
	button_ic = (153, 76, 0)
	button_ac = (204, 102, 0)
