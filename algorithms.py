# Breadth First Search
def BFS(Adj, source, target):

	# print("|| Breadth First Search ||")

	level = {source:0} # level of source is 0
	parent = {source:None} # parent of source is None
	i = 1
	frontier = [source] #  starting frontier is source
	shortest_path = [] # initialize empty list

	while frontier:
		next = []
		# print("\n\n### Level: %d" % (i-1)) # print current frontier level
		# print("Frontier to explore is: ")
		# print(frontier)

		for u in frontier:
			# print("\nCurrent node: " + u) # print current node
			# print(Adj[u])

			for v in Adj[u]:
				# print("\t- Current adjacent node: " + v)

				# if not already explored
				if v not in level:
					level[v] = i
					parent[v] = u
					next.append(v)

					# check if target found
					if v == target:
						# print("\nTarget found, interrupt BFS.")
						shortest_path = FSP(parent, source, target)
						# print("\nShortest path from " + source + " to " + target + " is:")
						# print(shortest_path)
						# print()
						return shortest_path, level

					# print("\t  Level of " + v + " is %d" % i)
					# print("\t  Parent of " + v + " is " + u)
					# print("\t  " + v + " appended to next.")

				# don't explore if already visited
				else:
					# print("\t  " + v + " is already explored.")
					pass


		frontier = next
		i = i+1 # increment i

	print("\n\n|| The graph is completely explored, BFS stops. Target has not been found. ||\n")
	return None, level


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
