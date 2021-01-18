'''
There are N network nodes, labelled 1 to N.

Given times, a list of travel times as directed edges times[i] = (u, v, w), where u is the source node, v is the target node, and w is the time it takes for a signal to travel from source to target.

Now, we send a signal from a certain node K. How long will it take for all nodes to receive the signal? If it is impossible, return -1.

Input: times = [[2,1,1],[2,3,1],[3,4,1]], N = 4, K = 2
Output: 2

(1)   ----   1 ------ (2 )
                        .
                        .
                        1
                        .
                        .
(4)   ----   1 -----  (3)

Time: O(ElogV)
Space: O(V+E)

Ref: https://leetcode.com/problems/network-delay-time/
'''
class Solution(object):
    #Djikstra Shortest path from a node.
    def networkDelayTime(self, times, N, K):
        #Process Input into an adjacency list
        nodes = set([x[0] for x in times] + [x[1] for x in times])
        adj   = dict( {x: [] for x in nodes})

        for a, b, w in times:
            adj[a].append((w,b))

        dist = {}
        heap = [(0, K)] #set distance of K to zero
        while heap:
            curr_dist, curr_node = heapq.heappop(heap)
            dist[curr_node] = curr_dist

            if len(dist) == N:
                break

            for neighbor_d, neighbor in adj[curr_node]:
                if neighbor not in dist:
                    heapq.heappush(heap, (curr_dist + neighbor_d, neighbor))

        if len(dist) != N:
            return -1
        else:
            return max(dist.values())




