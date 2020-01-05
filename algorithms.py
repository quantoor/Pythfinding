import math

####################### Breadth First Search #######################
class BFS:
	def __init__(self, Adj, source, target):
		self.Adj = Adj
		self.source = source
		self.target = target
		self.parent = {source:None} # parent of source is None
		self.nodeToLevelDict = {source:0} # level of source is 0
		self.levelToNodeDict = {0:[source]} # level 0 has only source

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
						
						if i in self.levelToNodeDict.keys():
							self.levelToNodeDict[i].append(v)
						else:
							self.levelToNodeDict[i] = [v]
						self.parent[v] = u
						next.append(v)

						# check if target found
						if v == self.target:
							shortest_path = self.FSP()
							return shortest_path, self.nodeToLevelDict, self.levelToNodeDict

			frontier = next
			i = i+1 # increment i

		print("\n|| The graph is completely explored, BFS stops. No target found. ||\n")
		return None, self.nodeToLevelDict, self.levelToNodeDict

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
		self.levelToNodeDict = {0:[source]} # level 0 has only source
		self.currentLevel = 1

	# Search with DFS
	def search(self):
		self.DFS_visit(self.source)
		return self.FPT(), self.nodeToLevelDict, self.levelToNodeDict

	# Recursive part of DFS
	def DFS_visit(self, s):
		for v in self.Adj[s]:
			if v not in self.parent:
				if self.targetFound:
					return
				# print("\tExploring %s " % v)
				self.exploredTiles.append(v) # append to explored tiles
				self.nodeToLevelDict[v] = self.currentLevel
				self.levelToNodeDict[self.currentLevel] = v
				self.currentLevel += 1

				# check if target found
				if v == self.target:
					# print("\t\tTarget found! Interrupt search")
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

		self.visited = [] # list of visited tiles

		# initialize dictionaries
		self.levelToIdDict = {} # keep track of order of explored tiles
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
			self.levelToIdDict[level] = index

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
					self.dist[edge] = newDist
					self.pq_push((edge, newDist))
					self.parent[edge] = index

		# print("\n|| The graph is completely explored, Dijkstra stops. ||\n")

		# pathToTargetList, idToLevelDict, exploredTiles
		return self.FSP(), self.dist, self.levelToIdDict, self.visited

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


def main():
	# Adjacency list
	Adj = {
		"a" : ("b","c"),
		"b" : ("d",),
		"c" : ("b","d"),
		"d" : ("e",),
		"e" : (None,)
	}

	# Weight dict
	W = {
		("a","b") : 4,
		("a","c") : 1,
		("c","b") : 2,
		("b","d") : 1,
		("c","d") : 5,
		("d","e") : 3
	}

	# Source
	source = "a"

	# Target
	target = "b"

	# Exectute Dijkstra
	dijkstra = Dijkstra(Adj, W, source, target)
	dist, parent, shortest_path = dijkstra.Dijkstra_main()
	print(dist)
	print(parent)
	print(shortest_path)
