
import pygame
from math import *
from config import Config
import algorithms


class Tile(pygame.Rect):
	tilesDict = {} # id to tile
	coordToIdDict = {} # coord to id
	neighborsDict = {} # id to neighbors ids
	counter = 1 # to keep track of the total number of the tiles
	Adj = {} # adjacency list
	shortestPathList = []
	levelDict = {}

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
		if self.id in Config.blocked_tiles:
			self.walkable = False

	def draw_tile(self, screen):
		# draw tiles
		x = self.x + Config.BORDER
		y = self.y + Config.BORDER

		if self.walkable:
			screen.blit(Image.tileWalkableImage, (x, y))
		else:
			screen.blit(Image.tileBlockedImage, (x, y))

		# draw source and target
		if self.id == Config.source:
			screen.blit(Image.tileSourceImage, (x, y))
		elif self.id == Config.target:
			screen.blit(Image.tileTargetImage, (x, y))

	def draw_text(self, screen):
		font = pygame.font.Font('freesansbold.ttf', 12)
		id_text = font.render(str(self.id), True, (255, 255, 255))
		screen.blit(id_text, (self.x+Config.TILE_SIZE//2-5+Config.BORDER, self.y+Config.TILE_SIZE//2-5+Config.BORDER))

		# print level
		if (self.walkable):
			font = pygame.font.Font('freesansbold.ttf', 10)
			# handle exception if tile is walkable but not reachable
			try:
				level_text = font.render(str(Tile.levelDict[self.id]), True, (255, 255, 255))
				screen.blit(level_text, (self.x+Config.BORDER+2, self.y+Config.BORDER+2))
			except:
				pass

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
			# print("\tneighbors are tiles " + str(Tile.neighborsDict[tile.id]))


	################################# DEBUG #################################
	@staticmethod
	def print_neighbors():
		for id in Tile.tilesDict.keys():
			if (Tile.tilesDict[id].walkable):
				# print("Tile %s has neighbors: " % id)
				print(Tile.neighborsDict[id])


class GameController:
	isSettingTargetSource = True
	isSettingWalkable = False

	@staticmethod
	def setNewTarget():
	    m_pos = pygame.mouse.get_pos()
	    m_x = (m_pos[0] - Config.BORDER) // Config.TILE_SIZE
	    m_y = (m_pos[1] - Config.BORDER) // Config.TILE_SIZE
	    try:
	        new_target_id = Tile.coordToIdDict[(m_x, m_y)]
	        Config.target = new_target_id
	        Tile.shortestPathList, Tile.levelDict = algorithms.BFS(Tile.neighborsDict, Config.source, Config.target)
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
	        Tile.shortestPathList, Tile.levelDict = algorithms.BFS(Tile.neighborsDict, Config.source, Config.target)
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

			Tile.build_neighbors_dict() # re-build adjacency list
			Tile.shortestPathList, Tile.levelDict = algorithms.BFS(Tile.neighborsDict, Config.source, Config.target)
		except:
			pass

	@staticmethod
	def isSettingTargetSourceMode():
		GameController.isSettingTargetSource = True
		GameController.isSettingWalkable = False
		print("is setting target source")

	@staticmethod
	def isSettingWalkableMode():
		GameController.isSettingTargetSource = False
		GameController.isSettingWalkable = True
		print("is setting walkable")


class Image:
	tileSourceImage = pygame.image.load("img/tile_source.png")
	tileTargetImage = pygame.image.load("img/tile_target.png")
	tileWalkableImage = pygame.image.load("img/tile_walkable.png")
	tileBlockedImage = pygame.image.load("img/tile_blocked.png")
	shortestPathImage = pygame.image.load("img/shortest_path.png")

	tileSourceImage = pygame.transform.scale(tileSourceImage, (Config.TILE_SIZE, Config.TILE_SIZE))
	tileTargetImage = pygame.transform.scale(tileTargetImage, (Config.TILE_SIZE, Config.TILE_SIZE))
	tileWalkableImage = pygame.transform.scale(tileWalkableImage, (Config.TILE_SIZE, Config.TILE_SIZE))
	tileBlockedImage = pygame.transform.scale(tileBlockedImage, (Config.TILE_SIZE, Config.TILE_SIZE))
	shortestPathImage = pygame.transform.scale(shortestPathImage, (Config.TILE_SIZE, Config.TILE_SIZE))

class Color:
	background = (255, 255, 102)
	white = (255,255,255)
	black = (0,0,0)
	button_ic = (153, 76, 0)
	button_ac = (204, 102, 0)
