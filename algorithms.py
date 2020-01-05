import math

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
		# print("|| Breadth First Search ||")
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
							return self.FSP(), self.nodeToLevelDict, self.frontierList

			frontier = next
			self.frontierList.append(frontier)
			i = i+1 # increment i

		return None, self.nodeToLevelDict, self.frontierList

	# Find Shortest Path from source to target
	def FSP(self):
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

	# Search with DFS
	def search(self):
		self.DFS_visit(self.source)
		return self.FPT(), self.nodeToLevelDict, self.frontierList

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

	# Find Path to target
	def FPT(self):
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
class Dijkstra:
	def __init__(self, Adj, W, source, target=None):
		self.Adj = Adj
		self.W = W
		self.source = source
		self.target = target
		self.targetFound = False
		N = len(Adj.keys()) # number of nodes

		self.levelToIdList = [0] # to show exploration
		self.levelToCostList = [0] # to draw cost when showing exploration
		self.visited = [] # list of visited tiles

		# initialize dictionaries
		self.dist = {}
		self.parent = {}
		for node in Adj.keys():
			# self.visited[node] = False
			self.dist[node] = math.inf
			self.parent[node] = None

		self.dist[source] = 0
		self.pq = [] # priority queue

	def search(self):
		level = 0
		self.pq_push((self.source, 0))

		while len(self.pq) > 0:
			index, minValue = self.pq_poll()
			self.visited.append(index)
			level += 1

			if index == self.target: # if the target is visited, interrupt search because min dist has been found
				self.targetFound = True
				break

			if minValue > self.dist[index]: # skip outdated values
				continue

			for edge in self.Adj[index]:
				if edge in self.visited: # skip if already visited
					continue

				newDist = self.dist[index] + self.W[index]
				if newDist < self.dist[edge]:
					self.levelToIdList.append([edge]) # to show relaxation
					self.levelToCostList.append(newDist) # to show relaxation

					self.dist[edge] = newDist
					self.pq_push((edge, newDist))
					self.parent[edge] = index

		# print("\n|| The graph is completely explored, Dijkstra stops. ||\n")

		# pathToTargetList, idToLevelDict, exploredTiles
		return self.FSP(), self.dist, self.levelToIdList, self.visited, self.levelToCostList

	# for inserting an element in the queue
	def pq_push(self, data):
		self.pq.append(data)

		# for popping an element based on Priority
	def pq_poll(self):
		# print("\n####################polling queue ",end="")
		# print(self.queue)
		# min = max(self.queue)[1]
		min = math.inf
		next_pair = None

		for pair in self.pq: # pair (node, distance)
			if pair[1] <= min:
				next_pair = pair
				min = pair[1]

		# print("node to return is ",end="")
		# print(next_node)
		self.pq.remove(next_pair)
		# print("now queue is ",end="")
		# print(self.queue)
		return next_pair

	# Find Shortest Path from source to target
	def FSP(self):
		if not self.targetFound:
			return None

		shortest_path = [self.target] # inverted path, starting from target back to source
		next_parent = self.parent[self.target]

		while True:
			if next_parent:
				shortest_path.append(next_parent)
				next_parent = self.parent[next_parent]
			else:
				return list(reversed(shortest_path)) # reverse list, from source to target
