"""
In a Binary Search Tree (BST), an Inorder Successor of a node is defined as the node with the smallest key greater than the key of the input node (see examples below). 
Given a node inputNode in a BST, you’re asked to write a function findInOrderSuccessor that returns the Inorder Successor of inputNode. 
If inputNode has no Inorder Successor, return null.

Ref: https://www.pramp.com/challenge/MW75pP53wAtzNPVLPG2b
"""

def find_in_order_successor(self, node):
    if node.right is None:
        if node.parent.val > node.val :
            return node.parent
        else:
            while node.parent.val < node.val:
                node = node.parent
            return node.parent
    else:
        node = node.right
        while node and node.left is not None:
            node = node.left
        return node