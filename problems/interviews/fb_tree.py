'''
Nodes in a Subtree
You are given a tree that contains N nodes, each containing an integer u which corresponds to a lowercase character c in the string s using 1-based indexing.
You are required to answer Q queries of type [u, c], where u is an integer and c is a lowercase letter. The query result is the number of nodes in the subtree of node u containing c.
Signature
int[] countOfNodes(Node root, ArrayList<Query> queries, String s)
Input
A pointer to the root node, an array list containing Q queries of type [u, c], and a string s
Constraints
N and Q are the integers between 1 and 1,000,000
u is an integer between 1 and N
s is of the length of N, containing only lowercase letters
c is a lowercase letter contained in string s
Node 1 is the root of the tree
Output
An integer array containing the response to each query
Example
        1(a)
        /   \
      2(b)  3(a)

s = "aba"
RootNode = 1
query = [[1, 'a']]
Note: Node 1 corresponds to first letter 'a', Node 2 corresponds to second letter of the string 'b', Node 3 corresponds to third letter of the string 'a'.
output = [2]
Both Node 1 and Node 3 contain 'a', so the number of nodes within the subtree of Node 1 containing 'a' is 2.
'''

import math
import collections

class Node:
    def __init__(self, data):
        self.val = data
        self.children = []

# Add any helper functions you may need here
def count_of_nodes(root, queries, s):
    def tuplify(root):
        if root:
            h[root.val].append(root.val)
            for child in root.children:
                h[root.val].extend(tuplify(child))
            return h[root.val]

    h = collections.defaultdict(list)
    tuplify(root)
    res = []
    for q in queries:
        u = q[0]
        c = q[1]
        children = [ x for x in h[u] if s[x-1] == c]
        res += [len(children)]

    return res

'''
Number of Visible Nodes
There is a binary tree with N nodes. You are viewing the tree from its left side and can see only the leftmost nodes at each level. Return the number of visible nodes.
Note: You can see only the leftmost nodes, but that doesn't mean they have to be left nodes. The leftmost node at a level could be a right node.
Signature
int visibleNodes(Node root) {
Input
The root node of a tree, where the number of nodes is between 1 and 1000, and the value of each node is between 0 and 1,000,000,000
Output
An int representing the number of visible nodes.
Example
            8  <------ root
           / \
         3    10
        / \     \
       1   6     14
          / \    /
         4   7  13            
output = 4
'''

def visible_nodes(root):
    def solve(root, d= 0):
        if root is not None:
            res[d].append( root.val )
            solve(root.left,  d+1)
            solve(root.right, d+1)

    res = collections.defaultdict(list)
    solve(root)
    return len( res.keys() )

