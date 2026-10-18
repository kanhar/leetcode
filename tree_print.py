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

def print_heap(arr,i=0,d=0):
    if i<0 or i >= len(arr):
        return

    l = i*2+1
    r = i*2+2

    print_heap(arr,l,d+1)
    print("   " * d,arr[i])
    print_heap(arr,r,d+1)


arr = [x for x in range(1,8)]
tree = create(arr)
print(tree.toStr())
