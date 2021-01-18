'''
     0 1 2
0    1 1 X
1    1 1 0
2    0 1 0

Input: 0,0 (Starting positions)
Obstacle: 0
Road: 1

Res = [ 0,2] [2,2]
'''

# Enter at starting position. Greedily check all paths that are traversable for a starbucks. If found. Terminate, Store path, else continue search. (do not repeat search)
import collections
global pathHash
import copy

pathHash = collections.defaultdict(list)

def solve(m, r,c, path = [], visited = set() ):
    if r not in range(0, len(m)) or c not in range(0, len(m[r])) or (r,c) in visited:
        return
    else:
        global pathHash
        if m[r][c] == 'X':
            pathHash[(r,c)].append(tuple(path))
        elif m[r][c] == 1:
            solve(m, r+1, c,   path + [(r,c)], visited | set([(r,c)])   )
            solve(m, r-1, c,   path + [(r,c)], visited | set([(r,c)])   )
            solve(m, r, c+1,   path + [(r,c)], visited | set([(r,c)])   )
            solve(m, r, c-1,   path + [(r,c)], visited | set([(r,c)])   )
            solve(m, r+1, c+1, path + [(r,c)], visited | set([(r,c)])   )


m = [ [1,1,'X'], [1,1,0], [0,1,'X']]
solve(m,0,0)
for k,val in pathHash.items():
    print(min(val, key = len), k)