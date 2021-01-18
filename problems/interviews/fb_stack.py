def isBalanced(s):
    op  = list( "{[(" )
    cl  = list( "}])" )
    h   = dict(zip(op, cl))
    stk = []

    for ch in s:
        if ch in h:
            stk.append(ch)
        else:
            if len(stk) == 0:
                return False

            if ch != h[stk.pop()]:
                return False

    return len(stk) == 0
  
print(isBalanced("{{[[(())]]}}") == True)
