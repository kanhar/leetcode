# graph class inspired by https://gist.github.com/econchick/4666413
# http://alexhwoods.com/dijkstra/
import collections
import math
from queue import Queue

class Graph:
    def __init__(self):
        self.nodes      = set()
        self.edges      = collections.defaultdict(list)                     # makes the default value for all nodes an empty list ( which will be a list of dictionaries )
        self.weights    = dict()
                
    def add_edge(self, nodeFrom, nodeTo, distance):
        if nodeFrom == nodeTo: pass                                         # no cycles allowed
        
        self.nodes.add(nodeFrom)
        self.nodes.add(nodeTo)        
         
        self.edges[nodeFrom].append(nodeTo)
        self.weights[(nodeFrom, nodeTo)] = distance

#KNM: TBD: Bug here. currNode reused incorrectly to hold min and hold the currnode. This doesnt work
def dijkstra(graph, start):    
    visited    = set()        
    distance   = dict.fromkeys(list(graph.nodes), math.inf)                 # distance represents the shortest distance of path from start -> currNode, for currNode in distance.
    previous   = dict.fromkeys(list(graph.nodes), None)    
    
    distance[start]    = 0                                                  # then we set the path length of the start vertex to 0
    while True:                                                             # while there exists a vertex currNode not in visited
        
        currNode    = min(graph.nodes - visited, default=-1)                # let currNode be the closest vertex that has not been visited...it will begin at 'start'
        if currNode == -1:
            break
                
        neighbors   = set(graph.edges[currNode]) - visited        
        for n in neighbors:                                                 # for each n of currNode not in visited            
            currDistance = distance[currNode] + graph.weights[(currNode,n)]
             
            if currDistance < distance[n]:                                  # is the new path from n through                
                distance[n] = currDistance                                  # since it's optimal, update the shortest path for n                
                previous[n] = currNode                                      # set the previous vertex of n to currNode ( reminding neighbors, thats where shortest dist so far is)
                                
        visited.add(currNode)
    
    return (distance, previous)

def bfs_RouteExists(graph, start, end):    
    q= Queue(len(graph.nodes))
    q.put(start)
    while not q.empty():
        curr  = q.get()                
        if( curr == end):                     
            return True
                        
        for e in graph.edges[curr]:            
            q.put(e)        
    return False

#Why cleaner? Safer, does not print, path is not shared. Somehow above path is shared
def dfs_GetAllPathsCleaner(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    
    pathList = []
    for node in graph.edges[start]:
        if node not in path:            
            pathList = pathList + dfs_GetAllPathsCleaner(graph, node, end, path)                        
    return pathList    


def shortest_path(graph, start, end):
    (distance, previous) = dijkstra(graph, start)  # @UnusedVariable
    
    path = []
    vertex = end    
    while vertex:
        path.append(vertex)
        vertex = previous[vertex]
    
    path.reverse()
    return path

G = Graph()

G.add_edge('a', 'b', 2)
G.add_edge('a', 'c', 8)
G.add_edge('a', 'd', 5)
G.add_edge('b', 'c', 1)
G.add_edge('c', 'e', 3)
G.add_edge('d', 'e', 4)

print(shortest_path(G, 'a', 'e'))
#print(bfs_RouteExists(G, 'a', 'e'))
#print(bfs_RouteExists(G, 'e', 'a'))


print("DFS", dfs_GetAllPathsCleaner(G, 'a', 'e') )
#print(dfs_RouteExists(G, 'e', 'a', list()))
#print(depthfirstsearch(G, 'a', 'e'))


'''    
    from functools import reduce
    self.edges2     = collections.defaultdict(list)                     # experimental
    self.edges2[nodeFrom].append( { nodeTo : distance } )               #experimental
    #Function way to extract edges from self.edges( if it were a list of dicts )
    def get_edges(self, currNode):
        return set().union(*(d.keys() for d in self.edges[currNode]))
        
    #Functional way to extract weights from self.edges, making self.weights obsolete( or extract key from a list of dictionaries )    
    def get_weight(self, nodeFrom, nodeTo):
        return reduce(lambda r, d: r.update(d) or r, self.edges[nodeFrom], {})[nodeTo]
        [queue.append(node) for node in [head.left, head.right] if node]
                '''
graph = {'A': set(['B', 'C']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['C', 'E'])}

def iterative_search(graph, start, goal, isDFS = True):
    ds = [(start, [start])]
    res   = []
    while ds:
        (vertex, path) = ds.pop() if isDFS else ds.pop(0)
        for i in graph[vertex] - set(path):
            if i == goal:
                res = res + [path+[i]]
            else:
                ds.append((i, path + [i]))
    return res
def dfs_paths_r(graph, start, goal, path=None):
    if path is None:
        path = [ start ]
    if start == goal:
        return( [ path ] )

    res = []
    for i in graph[start] - set(path):
        res = res + dfs_paths_r(graph, i, goal, path + [i])
    return res

print(list(iterative_search(graph, 'A', 'F', True)))
print(list(iterative_search(graph, 'A', 'F', False)))
print(list(dfs_paths_r(graph, 'A', 'F')))

