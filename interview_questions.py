import math

#Follow up: Given a map as a square, and a set of locations on the map, users are able to select a rectangle
# on the map and all of the locations on the map are returned
#How would you preprocess the map data so that the find operation for the locations in the inner rectangle
# can be done in less than O(n) time?
#Google
def findSquares():
    P = [ [0,0], [0,1], [1,0], [1,1], [2,0], [2,1],[0,2],[2,2]]

    h = set()
    for x,y in P:
        h.add((x,y))
    min_x = min([x[0] for x in P])
    max_x = max([x[0] for x in P])

    d     = 1
    while(d<=max_x-min_x):
        for x,y in P:
            top   = (x,   y+d)
            right = (x+d, y)
            diag  = (x+d, y+d)
            if top in h and right in h and diag in h:
                print('found square', (x,y), top,right,diag, d)
        d+=1

#Microsoft
def drawCircles():
    def setPixel(x,y):
        print(x,y,"\n")

    def drawCircle(r, xCenter, yCenter):
        x = 0;
        while (x<r):
            y = math.sqrt(r^2 - (x * x)) + 0.5; # round up
            x = x + 1

            setPixel(xCenter + x, yCenter + y)
            setPixel(xCenter + x, yCenter - y)
            setPixel(xCenter - x, yCenter + y)
            setPixel(xCenter - x, yCenter - y)
            setPixel(xCenter + y, yCenter + x)
            setPixel(xCenter + y, yCenter - x)
            setPixel(xCenter - y, yCenter + x)
            setPixel(xCenter - y, yCenter - x)

#Goldman
def merge_k_way(lists):
    import heapq
    heap  = [(l[0],i,0) for i,l in enumerate(lists) if len(l)> 0 ]
    heapq.heapify(heap)

    res = []
    while heap:
        smallest,k,i = heapq.heappop(heap)
        res.append(smallest)

        if i < len(lists[k])-1: #lets add new smallest from list K, at index i
            heapq.heappush(heap,(lists[k][i+1],k,i+1))

    return(res)


"""
File with ID1:123ID2:234..
Send message to ID1,ID2 spaced equally.
"""

import re
s = 'ID1:123ID2:234ID1:245'

arr = re.split('ID\d+:', s)
arr = [x for x in arr if x != '']
print(arr)

"""
Our application has a number of  projects that need to be built before they can be deployed. 
Projects may or may not depend on other projects.  
We need to know if we can build the projects -- e.g. if there is any circular dependency before we can get 
started on establishing CICD for the application.  

Given a list of projects, and pairs of dependencies, write a program to print the build order -- if there 
is circular dependencies, print as an error,

INPUTFILE:
    Line1:  project names delimited by comma
    Line2+:  Project1, Project2         -- Project1 must be built before Project2
                  ….
OUTPUT to STDOUT:   Build order of the projects

For example:
INPUTFILE: 

A, B, C, D, E, F, J
A, B
B, C
D, C
D, A
E, F
D,F
        
OUTPUT TO STDOUT: J,  D, A, B, C, E, F
"""
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
    raise ValueError("There likely exists a cycle")

print(res) #Prints: ['D', 'E', 'J', 'A', 'F', 'B', 'C']

"""

See if parentheses are valid
Get Maximum depth
Get Maximum breadth

Ref: https://leetcode.com/problems/maximum-nesting-depth-of-the-parentheses/
"""


"""
Merge K Sorted Arrays
Ref: https://leetcode.com/discuss/interview-question/617596/facebook-onsite-merge-k-sorted-arrays
"""

import heapq
def solve(arr):
    h = []
    for i in range(0, len(arr)):
        heapq.heappush(h, (arr[i][0], i, 0))

    res = []
    while h:
        val, arrayNum, arrayIndex = heapq.heappop(h)
        res.append(val)

        if arrayIndex +1 < len(arr[arrayNum]):
            heapq.heappush(h, (arr[arrayNum][arrayIndex+1], arrayNum, arrayIndex+1))

    return res

arr = [ [ 1,2,3 ], [4,5,6], [0,1,2]]
print(solve(arr))

"""
Ref: Interview: Find Median O(log(n)) time.
"""
import heapq

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        def findnsmallset(arr, n):
            if len(arr)==1:
                return arr[0]
            if len(arr)==0:
                return -1
            P = arr[int(len(arr)/2)]
            smaller = [x for x in arr if x < P]
            bigger = [x for x in arr if x > P]
            equal = [x for x in arr if x == P]
            if n < len(smaller):
                return findnsmallset(smaller,n)
            elif len(smaller) <= n < len(smaller)+len(equal):
                return P
            else:
                return findnsmallset(bigger,n-len(smaller)-len(equal))

        def median(arr):
            m = len(arr)//2
            if len(arr)%2==1: #even
                return findnsmallset(arr,m)
            else:
                return int((findnsmallset(arr,m) + findnsmallset(arr,m-1))/2)
        return findnsmallset(nums,len(nums)-k)
