# Breadth First Search
def BFS(Adj, source, target):

	# print("|| Breadth First Search ||")

	nodeToLevelDict = {source:0} # level of source is 0
	levelToNodeDict = {0:[source]} # level 0 has only source
	parent = {source:None} # parent of source is None
	i = 1
	frontier = [source] #  starting frontier is source
	shortest_path = [] # initialize empty list

	while frontier:
		next = []

		for u in frontier:
			for v in Adj[u]:

				# if not already explored
				if v not in nodeToLevelDict:
					nodeToLevelDict[v] = i
					if i in levelToNodeDict.keys():
						levelToNodeDict[i].append(v)
					else:
						levelToNodeDict[i] = [v]
					parent[v] = u
					next.append(v)

					# check if target found
					if v == target:
						shortest_path = FSP(parent, source, target)
						return shortest_path, nodeToLevelDict, levelToNodeDict

		frontier = next
		i = i+1 # increment i

	print("\n\n|| The graph is completely explored, BFS stops. Target has not been found. ||\n")
	return None, nodeToLevelDict, levelToNodeDict


# Find Shortest Path from source to target
def FSP(parent, source, target):
	shortest_path = [target] # inverted path, starting from target back to source
	next_parent = parent[target]

	while True:

		if next_parent:
			shortest_path.append(next_parent)
			next_parent = parent[next_parent]
		else:
			return list(reversed(shortest_path)) # reverse list, from source to target
