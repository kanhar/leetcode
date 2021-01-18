'''
There are N network nodes, labelled 1 to N.

Given times, a list of travel times as directed edges times[i] = (u, v, w), where u is the source node, v is the target node, and w is the time it takes for
a signal to travel from source to target.

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

Bellman Ford
Time: O(VE)
Space: O(V)
'''
class Solution(object):
    #Bellman Ford: Single Source Shortest Path ( can handle negative weight cycles )
    def networkDelayTime(self, times, N, K):
        nodes     = set([x[0] for x in times] + [x[1] for x in times])
        distance  = dict( {x: float('inf') for x in nodes})

        if len(nodes) < N: #Good check to ensure Graph is connected, i.e. no missing nodes.
            return -1

        distance[K] = 0 #set distance of K to zero
        for _ in range(N-1):
            for source, dest, w in times:
                distance[dest] = min( distance[source] + w, distance[dest] )

        for source, dest,w in times:
            if distance[dest] > distance[source]+w:
                raise ValueError('Graph contains a negative weight cycle')

        if max(distance.values()) == float('inf'):
            return -1
        else:
            return max(distance.values())