import math
from bean import Tile
from config import Config

# Base abstract class
class Algorithm:
	def search():
		pass

	def find_path():
		pass


####################### Breadth First Search #######################
class BFS:
	def __init__(self, Adj, source, target):
		self.Adj = Adj
		self.source = source
		self.target = target
		self.targetFound = False
		self.parent = {source:None} # parent of source is None
		self.nodeToLevelDict = {source:0} # level of source is 0

		# each element of the list represents a level and has a list with all nodes belonging to that level (frontier)
		# e.g. level 0 has list of elements [source]
		self.frontierList = [[source]]

	def search(self):
		i = 1
		frontier = [self.source] #  starting frontier is source

		while frontier:
			next = []

			for u in frontier:
				for v in self.Adj[u]:

					# if not already explored
					if v not in self.nodeToLevelDict:
						self.nodeToLevelDict[v] = i
						self.parent[v] = u
						next.append(v)

						# check if target found
						if v == self.target:
							self.targetFound = True
							self.frontierList.append(next)
							return self.find_path(), self.nodeToLevelDict, self.frontierList

			frontier = next
			self.frontierList.append(frontier)
			i = i+1 # increment i

		return None, self.nodeToLevelDict, self.frontierList

	def find_path(self):
		shortest_path = [self.target] # inverted path, starting from target back to source
		next_parent = self.parent[self.target]

		while True:
			if next_parent:
				shortest_path.append(next_parent)
				next_parent = self.parent[next_parent]
			else:
				return list(reversed(shortest_path)) # reverse list, from source to target


####################### Depth First Search #######################
class DFS:
	def __init__(self, Adj, source, target=None):
		self.Adj = Adj
		self.source = source
		self.target = target
		self.parent = {source:None}
		self.targetFound = False
		self.exploredTiles = [self.source]
		self.nodeToLevelDict = {source:0} # level of source is 0
		self.frontierList = [[source]] # frontier list (for DFS frontier has only 1 node but it is still a list)
		self.currentLevel = 1

	def search(self):
		self.DFS_visit(self.source)
		return self.find_path(), self.nodeToLevelDict, self.frontierList

	# Recursive part of DFS
	def DFS_visit(self, s):
		for v in self.Adj[s]:
			if v not in self.parent:

				if self.targetFound:
					return

				self.exploredTiles.append(v) # append to explored tiles
				self.nodeToLevelDict[v] = self.currentLevel
				self.frontierList.append([v])
				self.currentLevel += 1

				# check if target found
				if v == self.target:
					self.targetFound = True

				self.parent[v] = s
				self.DFS_visit(v)

	def find_path(self):
		if not self.targetFound:
			return None

		path = [self.target] # inverted path, starting from target back to source
		next_parent = self.parent[self.target]

		while True:
			if next_parent:
				path.append(next_parent)
				next_parent = self.parent[next_parent]
			else:
				return list(reversed(path)) # reverse list, from source to target


####################### Dijkstra #######################
# optimal but non efficient
class Dijkstra: # if target!=None it is Uniform cost search
	def __init__(self, Adj, W, source, target=None):
		self.Adj = Adj
		self.W = W
		self.source = source
		self.target = target
		self.targetFound = False
		N = len(Adj.keys()) # number of nodes

		self.levelToIdList = [[source]] # to show exploration
		self.levelToCostList = [0] # to draw cost when showing exploration
		self.visitedList = [source] # visited nodes that are expanded
		self.exploredList = [source] # visited means the algorithm looked at it, not necessarily expanded

		# initialize dictionaries
		self.distDict = {} # maps id to g(n)
		self.parentDict = {}
		for node in Adj.keys():
			self.distDict[node] = math.inf
			self.parentDict[node] = None

		self.distDict[source] = 0
		self.pq = {} # priority queue

	def search(self):
		level = 0
		self.pq[self.source] = 0

		while len(self.pq) > 0:
			index = poll(self.pq)
			self.visitedList.append(index)
			level += 1

			if index == self.target: # if the target is visited, interrupt search because min dist has been found
				self.targetFound = True
				break

			newDist = self.distDict[index] + self.W[index] # which is self.distDict[edge]
			for edge in self.Adj[index]:
				if edge not in self.visitedList and edge not in self.pq.keys(): # not visited and not in pq
					self.exploredList.append(edge)
				elif edge in self.pq.keys() and newDist < self.pq[edge]:
					pass
				else: # edge in frontier but worse distance
					continue

				self.levelToIdList.append([edge]) # to show relaxation
				self.levelToCostList.append(newDist) # to show relaxation
				self.distDict[edge] = newDist
				self.parentDict[edge] = index
				self.pq[edge] = newDist

		return self.find_path(), self.distDict, self.levelToIdList, self.exploredList, self.levelToCostList

	def find_path(self):
		if not self.targetFound:
			return None

		shortest_path = [self.target] # inverted path, starting from target back to source
		next_parent = self.parentDict[self.target]

		while True:
			if next_parent:
				shortest_path.append(next_parent)
				next_parent = self.parentDict[next_parent]
			else:
				return list(reversed(shortest_path)) # reverse list, from source to target


####################### Best-First Search #######################
# non optimal but often efficient
class B_FS:
	def __init__(self, Adj, W, source, target):
		self.Adj = Adj
		self.W = W
		self.source = source
		self.target = target
		self.targetFound = False
		N = len(Adj.keys()) # number of nodes

		self.levelToIdList = [[source]] # to show exploration
		self.levelToCostList = [0] # to draw cost when showing exploration
		self.visitedList = [source] # visited nodes that are expanded
		self.exploredList = [source] # visited means the algorithm looked at it, not necessarily expanded

		# initialize dictionaries
		self.distDict = {} # maps id to g(n)
		self.parentDict = {}
		self.h = {} # heuristic function h(n)
		for node in Adj.keys():
			self.distDict[node] = math.inf
			self.parentDict[node] = None
			self.h[node] = compute_distance(node, target)

		self.distDict[source] = 0
		self.pq = {} # priority queue

	def search(self):
		level = 0
		self.pq[self.source] = self.h[self.source]

		while len(self.pq) > 0:
			index = poll(self.pq)
			self.visitedList.append(index)
			level += 1

			if index == self.target: # if the target is visited, interrupt search because min dist has been found
				self.targetFound = True
				break

			newDist = self.distDict[index] + self.W[index] # which is self.distDict[edge]
			for edge in self.Adj[index]:
				if edge not in self.visitedList and edge not in self.pq.keys():
					self.exploredList.append(edge)
				elif edge in self.pq.keys() and self.pq[edge] > newDist:
					pass
				else:
					continue

				self.levelToIdList.append([edge]) # to show relaxation
				self.levelToCostList.append(newDist) # to show relaxation
				self.distDict[edge] = newDist
				self.parentDict[edge] = index
				self.pq[edge] = self.h[edge]

		return self.find_path(), self.distDict, self.levelToIdList, self.exploredList, self.levelToCostList

	def find_path(self):
		if not self.targetFound:
			return None

		shortest_path = [self.target] # inverted path, starting from target back to source
		next_parent = self.parentDict[self.target]

		while True:
			if next_parent:
				shortest_path.append(next_parent)
				next_parent = self.parentDict[next_parent]
			else:
				return list(reversed(shortest_path)) # reverse list, from source to target


####################### A* #######################
# optimal and efficient
class A_star:
	def __init__(self, Adj, W, source, target):
		self.Adj = Adj
		self.W = W
		self.source = source
		self.target = target
		self.targetFound = False
		N = len(Adj.keys()) # number of nodes

		self.levelToIdList = [[source]] # to show exploration
		self.levelToCostList = [0] # to draw cost when showing exploration
		self.visitedList = [source] # visited nodes that are expanded
		self.exploredList = [source] # visited means the algorithm looked at it, not necessarily expanded

		# initialize dictionaries
		self.distDict = {} # maps id to g(n)
		self.parentDict = {}
		self.h = {} # heuristic function h(n)
		for node in Adj.keys():
			self.distDict[node] = math.inf
			self.parentDict[node] = None
			self.h[node] = compute_distance(node, target)

		self.distDict[source] = 0
		self.pq = {} # priority queue

	def search(self):
		# print("\n\n### A* starting search")
		level = 0
		self.pq[self.source] = 0 + self.h[self.source] # (n, f = g + h)

		while len(self.pq) > 0:
			index = poll(self.pq)
			self.visitedList.append(index)
			# print("visiting node %s" % index)
			level += 1

			if index == self.target: # if the target is visited, interrupt search because min dist has been found
				self.targetFound = True
				break

			for edge in self.Adj[index]:
				new_f = self.distDict[index] + self.W[index] + self.h[edge]
				newDist = self.distDict[index] + self.W[index]
				# print("\n\tlooking at node %s" % edge)

				if (edge not in self.visitedList) and (edge not in self.pq.keys()):
					# print("\tnode %s is not visited or in queue. g = %f, h = %f, f = %f" % (edge, newDist, self.h[edge], new_f))
					self.exploredList.append(edge)
					self.levelToIdList.append([edge]) # to show relaxation
					self.levelToCostList.append(newDist) # to show relaxation
					self.distDict[edge] = newDist
					self.parentDict[edge] = index
					self.pq[edge] = newDist + self.h[edge]

				elif (edge in self.pq.keys()) and (new_f < self.pq[edge]):
					# print("\n\tnode %s already in queue with higher path cost -> relax edge" % edge)
					# print("\tnode %s path cost was: %f" % (edge, self.pq[edge]))
					# print("\tnode %s path cost now is: %f" % (edge, new_f))
					self.levelToIdList.append([edge]) # to show relaxation
					self.levelToCostList.append(newDist) # to show relaxation
					self.distDict[edge] = newDist
					self.parentDict[edge] = index
					self.pq[edge] = newDist + self.h[edge]

				# else:
				# 	print("\n\tnode %s already in queue with better path cost -> do not relax" % edge)
				# 	print("\tnew_f is: %f" % (new_f))
				# 	print("\tpath cost was: %f" % (self.distDict[edge] + self.h[edge]))

		return self.find_path(), self.distDict, self.levelToIdList, self.exploredList, self.levelToCostList

	def find_path(self):
		if not self.targetFound:
			return None

		shortest_path = [self.target] # inverted path, starting from target back to source
		next_parent = self.parentDict[self.target]

		while True:
			if next_parent:
				shortest_path.append(next_parent)
				next_parent = self.parentDict[next_parent]
			else:
				return list(reversed(shortest_path)) # reverse list, from source to target


####################### Util #######################
class PriorityQueue(dict):
	def __init__(self):
		self.queue = {}

	# for inserting an element in the queue
	def push(self, node, value):
		self.queue[node] = value

	# for popping an element based on Priority
	def poll(self):
		min = math.inf
		next_node = None

		for node in self.queue.keys():
			if self.queue[node] <= min:
				next_node = node
				min = self.queue[node]

		del self.queue[next_node]
		return next_node

	def __len__(self):
		return len(self.queue)


def poll(dic):
	min = math.inf
	next_node = None
	for node in dic.keys():
		if dic[node] <= min:
			next_node = node
			min = dic[node]
	del dic[next_node]
	return next_node


def compute_distance(tile1, tile2):
	tile1Pos = Tile.idToCoordDict[tile1]
	tile2Pos = Tile.idToCoordDict[tile2]
	# Manhattan distance
	return (abs(tile1Pos[0]-tile2Pos[0]) + abs(tile1Pos[1]-tile2Pos[1])) / Config.TILE_SIZE
