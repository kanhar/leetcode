class TreeNode:

    def __init__(self, value=None, left=None, right=None, parent=None):
        self.right = right
        self.left = left
        self.val = value
        self.parent = parent

    def toStr(self, depth=0):
        ret = ""

        if self.right != None:
            ret += self.right.toStr(depth + 1)

        if( self.val is not None):
            ret += "\n" + ("   "*depth) + str(self.val)

        if self.left != None:
            ret += self.left.toStr(depth + 1)

        return ret

def create(arr, start=0, end=None):
    if end is None:
        end = len(arr)-1

    if start > end:
        return None
    mid         = int((start + end) / 2)
    return TreeNode(arr[mid], create(arr, start, mid - 1), create(arr, mid + 1, end))

def inOrder(root):
    res = []
    tmp = root
    def solve(root):
        if root:
            solve(root.left)
            res.append(root.val)
            solve(root.right)

    solve(tmp)
    return res

def preOrder(root):
    res = []
    tmp = root
    def solve(root):
        if root:
            res.append(root.val)
            solve(root.right)
            solve(root.right)

    solve(tmp)
    return res

def postOrder(root):
    res = []
    tmp = root
    def solve(root):
        if root:
            solve(root.right)
            solve(root.left)
            res.append(root.val)

    solve(tmp)
    return res

arr = [x for x in range(1,8)]
tree = create(arr)
print(tree.toStr())

print(inOrder(tree))
print(preOrder(tree))
print(postOrder(tree))

