"""
A city's skyline is the outer contour of the silhouette formed by all the buildings in that city
when viewed from a distance.
Now suppose you are given the locations and height of all the buildings as shown on a cityscape
photo (Figure A), write a program to output the skyline formed by these buildings collectively (Figure B).
"""

#TLE, and out of memory
import heapq


class Solution:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        res = [0]*(buildings[-1][1]+1)
        for b in buildings:
            for i in range(b[0], b[1]+1):
                res[i] = max(res[i], b[2] )
        res = res + [0]

        final = []
        prevHeight = 0
        for idx, height in enumerate(res):
            if height != prevHeight:
                if prevHeight < height:
                    final += [[idx,height]]
                else:
                    final += [[idx-1,height]]
                prevHeight = height
        return final

#Heap has Format (-height, right)
def getRight(heap):
    return heap[1]

def getHeight(heap):
    return -heap[0]

class Solution:
    def getSkyline(self, buildings: List[List[int]]) -> List[List[int]]:
        events =  [(L, H, R) for L, R, H in buildings]
        events += [(R, -1, _) for _, R, _ in buildings]              # Buildings with No height, only position
        events.sort()

        res  = [[0,0]]
        heap = []

        for i,(left, height, right) in enumerate(events):

            if height >= 0:                                         # Start of building
                heapq.heappush(heap, (-height, right))              # Largest Height first

            if i < len(events)-1 and left == events[i+1][0]:        # Skip duplicates
                continue

            while heap and getRight(heap[0]) <= left:               # Remove from heap buildings that end before = current left
                heapq.heappop(heap)

            if not heap:
                res.append([left, 0])
            elif res[-1][1] != getHeight( heap[0] ):
                res.append([left, getHeight( heap[0] )])

        return res[1:]