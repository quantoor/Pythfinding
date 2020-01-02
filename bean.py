
import pygame
from math import *

pygame.mixer.init()

class Config:
	ROWS = 5 # number of rows
	COLS = 5 # number of cols
	TILE_SIZE = 100 # px
	FPS = 60
	source = "1"
	target = "25"
	blocked_tiles = ["7", "9", "10", "12", "19", "22", "24"]


class Image:
	tileSourceImage = pygame.image.load("img/tile_source.png")
	tileTargetImage = pygame.image.load("img/tile_target.png")
	tileWalkableImage = pygame.image.load("img/tile_walkable.png")
	tileBlockedImage = pygame.image.load("img/tile_blocked.png")


class Tile(pygame.Rect):
	tilesDict = {} # id to tile
	posToIdDict = {} # position to id
	neighborsDict = {} # id to neighbors ids
	counter = 1 # to keep track of the total number of the tiles
	Adj = {} # adjacency list
	shortestPath = []
	levelDict = {}

	def __init__(self, x, y, TILE_W, TILE_H):
		pygame.Rect.__init__(self, x, y, TILE_W, TILE_H)
		self.id = str(Tile.counter)
		Tile.counter += 1 # increase total tile counter
		print("Created tile %s at pos (%d, %d)" % (self.id, x, y))

		self.position = (x,y)
		self.width = TILE_W
		self.height = TILE_H

		Tile.tilesDict[self.id] = self # map this id to this tile
		Tile.posToIdDict[self.position] = self.id # map this position to this id

		self.walkable = True
		if self.id in Config.blocked_tiles:
			self.walkable = False

	def draw_tile(self, screen):
		if self.walkable:
			screen.blit(Image.tileWalkableImage, (self.x, self.y))
		else:
			screen.blit(Image.tileBlockedImage, (self.x, self.y))
		if self.id == Config.source:
			screen.blit(Image.tileSourceImage, (self.x, self.y))
		elif self.id == Config.target:
			screen.blit(Image.tileTargetImage, (self.x, self.y))

	def draw_text(self, screen):
		font = pygame.font.Font('freesansbold.ttf', 16)
		id_text = font.render(str(self.id), True, (255, 255, 255))
		screen.blit(id_text, (self.x+45, self.y+45))

		if (self.walkable):
			font = pygame.font.Font('freesansbold.ttf', 12)
			level_text = font.render(str(Tile.levelDict[self.id]), True, (255, 255, 255))
			screen.blit(level_text, (self.x+2, self.y+2))

	@staticmethod
	def build_neighbors_dict():
		for tile in Tile.tilesDict.values():
			if not tile.walkable: # skip tile if not walkable
				continue
			x = tile.position[0]
			y = tile.position[1]
			w = tile.width
			h = tile.height
			neighborsList = []

			print("\nTile %s " % tile.id)
			neighborPos = (x, y-h) # above
			if ( neighborPos in Tile.posToIdDict.keys() ):
				if (Tile.tilesDict[Tile.posToIdDict[neighborPos]].walkable):
					neighborsList.append(Tile.posToIdDict[neighborPos])
					print("\thas neighbor above " + str(neighborPos))

			neighborPos = (x+w, y) # right
			if ( neighborPos in Tile.posToIdDict.keys() ):
				if (Tile.tilesDict[Tile.posToIdDict[neighborPos]].walkable):
					neighborsList.append(Tile.posToIdDict[neighborPos])
					print("\thas neighbor right " + str(neighborPos))

			neighborPos = (x, y+h) # below
			if ( neighborPos in Tile.posToIdDict.keys() ):
				if (Tile.tilesDict[Tile.posToIdDict[neighborPos]].walkable):
					neighborsList.append(Tile.posToIdDict[neighborPos])
					print("\thas neighbor below " + str(neighborPos))

			neighborPos = (x-w, y) # left
			if ( neighborPos in Tile.posToIdDict.keys() ):
				if (Tile.tilesDict[Tile.posToIdDict[neighborPos]].walkable):
					neighborsList.append(Tile.posToIdDict[neighborPos])
					print("\thas neighbor left " + str(neighborPos))

			Tile.neighborsDict[tile.id] = neighborsList # map tile id to neighbor id
			print("\tneighbors are tiles " + str(Tile.neighborsDict[tile.id]))


	################################# DEBUG #################################
	@staticmethod
	def print_neighbors():
		for id in Tile.tilesDict.keys():
			if (Tile.tilesDict[id].walkable):
				print("Tile %s has neighbors: " % id)
				print(Tile.neighborsDict[id])
