import math

#Follow up: Given a map as a square, and a set of locations on the map, users are able to select a rectangle on the map and all of the locations on the map are returned
#How would you preprocess the map data so that the find operation for the locations in the inner rectangle can be done in less than O(n) time?
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

