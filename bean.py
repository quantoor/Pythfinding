
import pygame
from math import *

pygame.mixer.init()


class Image():
	tileWalkableImage = pygame.image.load("img/tile_walkable.png")
	tileBlockedImage = pygame.image.load("img/tile_blocked.png")


class Tile(pygame.Rect):
	tilesDict = {} # id to tile
	posToIdDict = {} # position to id
	neighborsDict = {} # id to neighbors ids
	counter = 1 # to keep track of the total number of the tiles


	def __init__(self, x, y, TILE_W, TILE_H):
		pygame.Rect.__init__(self, x, y, TILE_W, TILE_H)
		self.id = Tile.counter
		Tile.counter += 1 # increase total tile counter
		print("Created tile %d at pos (%d, %d)" % (self.id, x, y))

		self.position = (x,y)
		self.width = TILE_W
		self.height = TILE_H

		Tile.tilesDict[self.id] = self # map this id to this tile
		Tile.posToIdDict[self.position] = self.id # map this position to this id


	def draw_tile(self, screen):
		screen.blit(Image.tileWalkableImage, (self.x, self.y))

		font = pygame.font.Font('freesansbold.ttf', 16)
		text = font.render(str(self.id), True, (255, 255, 255))
		screen.blit(text, (self.x+45, self.y+45))

	@staticmethod
	def build_neighbors_dict():
		for tile in Tile.tilesDict.values():
			x = tile.position[0]
			y = tile.position[1]
			w = tile.width
			h = tile.height
			neighborsList = []

			print("\nTile %d " % tile.id)
			neighborPos = (x, y-h) # above
			if ( neighborPos in Tile.posToIdDict.keys() ):
				neighborsList.append(Tile.posToIdDict[neighborPos])
				print("\thas neighbor above " + str(neighborPos))

			neighborPos = (x+w, y) # right
			if ( neighborPos in Tile.posToIdDict.keys() ):
				neighborsList.append(Tile.posToIdDict[neighborPos])
				print("\thas neighbor right " + str(neighborPos))

			neighborPos = (x, y+h) # below
			if ( neighborPos in Tile.posToIdDict.keys() ):
				neighborsList.append(Tile.posToIdDict[neighborPos])
				print("\thas neighbor below " + str(neighborPos))

			neighborPos = (x-w, y) # left
			if ( neighborPos in Tile.posToIdDict.keys() ):
				neighborsList.append(Tile.posToIdDict[neighborPos])
				print("\thas neighbor left " + str(neighborPos))

			Tile.neighborsDict[tile.id] = neighborsList # map tile id to neighbor id
			print("\tneighbors are tiles " + str(Tile.neighborsDict[tile.id]))


	################################# debug #################################
	@staticmethod
	def print_neighbors():
		for id in Tile.tilesDict.keys():
			print("Tile %d has neighbors: " % id)
			print(Tile.neighborsDict[id])
