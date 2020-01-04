####################### Breadth First Search #######################
class BFS:
	def __init__(self, Adj, source, target):
		self.Adj = Adj
		self.source = source
		self.target = target
		self.parent = {source:None} # parent of source is None
		self.nodeToLevelDict = {source:0} # level of source is 0
		self.levelToNodeDict = {0:[source]} # level 0 has only source

	def BFS_main(self):
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
		self.target_found = False
		self.exploredTiles = [self.source]
		self.nodeToLevelDict = {source:0} # level of source is 0
		self.levelToNodeDict = {0:[source]} # level 0 has only source
		self.currentLevel = 1

	# Search with DFS
	def DFS_main(self):
		# print("|| DFS starts exploring ... ||")
		# print("\tStarting at " + self.source)
		self.DFS_visit(self.source)
		# print("\n|| The graph is completely explored, DFS stops. ||\n")

		# if self.target_found:
		# 	print("Path from " + self.source + " to " + self.target + " is:")
		# 	print(self.FPT())
		# else:
		# 	print("No target found.")

		return self.parent, self.nodeToLevelDict, self.levelToNodeDict

	# Recursive part of DFS
	def DFS_visit(self, s):
		for v in self.Adj[s]:
			if v not in self.parent:
				if self.target_found:
					return
				# print("\tExploring %s " % v)
				self.exploredTiles.append(v) # append to explored tiles
				self.nodeToLevelDict[v] = self.currentLevel
				self.levelToNodeDict[self.currentLevel] = v
				self.currentLevel += 1

				# check if target found
				if v == self.target:
					# print("\t\tTarget found! Interrupt search")
					self.target_found = True

				self.parent[v] = s
				self.DFS_visit(v)

	# Find Path to target
	def FPT(self):
		path = [self.target] # inverted path, starting from target back to source
		next_parent = self.parent[self.target]

		while True:
			if next_parent:
				path.append(next_parent)
				next_parent = self.parent[next_parent]
			else:
				return list(reversed(path)) # reverse list, from source to target
