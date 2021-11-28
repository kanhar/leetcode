def createLeetTree(arr, index=0):
    if index >= len(arr) or arr[index] == None:
        return None

    left  = index*2+1
    right = index*2+2
    parent = TreeNode(arr[index], createLeetTree(arr, left), createLeetTree(arr, right))

    return parent
