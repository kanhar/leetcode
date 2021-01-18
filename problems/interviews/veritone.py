import collections

nodes = [ 'A', 'B', 'C', 'D', 'E', 'F', 'J']
arr = [
    ['A', 'B'],
    ['B', 'C'],
    ['D', 'C'],
    ['D', 'A'],
    ['E', 'F'],
    ['D', 'F'],
]

# Create Graph, and Indeg Count for each Node.
graph = collections.defaultdict(list)
indeg = {x:0 for x in nodes}
for a, b in arr:
    graph[a].append(b)
    indeg[b] +=1

res = []

# Start with All nodes that have no indegree. No inward dep. link.
q = [x for x in indeg if indeg[x] == 0]
while q:
    curr = q.pop(0)
    res.append(curr)

    # We have essentially removed 'curr' from Graph above.
    #   -   Recalculate indegree of all of 'curr''s outward neighbors ( i.e. subtract by one )
    #   -   If as a result of above, neighbors indegree becomes 0, add to Queue.
    for neighbor in graph[curr]:
        indeg[neighbor] -= 1
        if indeg[neighbor] == 0:
            q.append(neighbor)

# If despite above algoithm total nodes accumulated, are less than total, something bad happened. Likely a cycle.
if len(res) < len(indeg):
    raiseError("There likely exists a cycle")

print(res) #Prints: ['D', 'E', 'J', 'A', 'F', 'B', 'C']


