{: .no_toc}
# Stack
Practise here: [Leetcode](https://leetcode.com/list/?selectedList=9duv7mlj)

- TOC
{:toc}

### [Basic Calculator](https://leetcode.com/problems/basic-calculator/)

> Input: "(1+(4+5+2)-3)+(6+8)". <BR>
> Output: 23

See [LC: Python-Basic-Calculator-I-II-III-easy-solution-detailed-explanation](https://leetcode.com/problems/basic-calculator/discuss/1456850/Python-Basic-Calculator-I-II-III-easy-solution-detailed-explanation)
<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def calculate(self, s):
        def update(op, v):
            if op == "+": stack.append(v)
            if op == "-": stack.append(-v)
            if op == "*": stack.append(stack.pop() * v)           #for BC II and BC III
            if op == "/": stack.append(int(stack.pop() / v))      #for BC II and BC III
    
        it, num, stack, sign = 0, 0, [], "+"
        
        while it < len(s):
            if s[it].isdigit():
                num = num * 10 + int(s[it])
            elif s[it] in "+-*/":
                update(sign, num)
                num, sign = 0, s[it]
            elif s[it] == "(":                                        # For BC I and BC III
                num, j = self.calculate(s[it + 1:])
                it = it + j
            elif s[it] == ")":                                        # For BC I and BC III
                update(sign, num)
                return sum(stack), it + 1
            it += 1
        update(sign, num)
        return sum(stack)
```

</details>
<BR>

### [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/)

> Given a string containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

<details><summary markdown="span">Execute!</summary>

```python
class Solution(object):
    def isValid(self, s):
        d = dict(zip("([{",")]}" ) )
        stk = []
        for b in s:
            if b in d.keys():
                stk.append(b)
            elif b in d.values():
                if stk == [] or b != d[stk.pop()]:
                    return False

        return len(stk)==0
```

</details>
<BR>


### [Decode-String](https://leetcode.com/problems/decode-string/)

> Given an encoded string, return its decoded string.
> See also [Regex.html#decode-string](https://kanhar.github.io/leetcode/problems/Misc/Regex.html#decode-string)

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def decodeString(self, s: str) -> str:

        stk = []
        curr_num = 0
        curr_str = ''

        for i in s:
            if i.isdigit():
                curr_num = curr_num*10 + int(i)

            elif i.isalpha():
                curr_str += i

            elif i == '[':
                stk.append((curr_num, curr_str))
                curr_num = 0
                curr_str = ''

            elif i == ']':
                prev_num, prev_str = stk.pop()
                curr_str = prev_str + prev_num*curr_str

        return curr_str
```

DFS Approach (implicit Stack)

```python
class Solution:
    def decodeString(self, s):
        def dfs(s):
            nonlocal i
            r = []

            while i < len(s): 
                if s[i] == ']':
                    i +=1 
                    return ''.join(r)

                elif s[i] == '[':
                    i += 1 
                    sub = dfs(s) 
                    r.append(sub * n)

                elif s[i].isdigit():
                    n = 0 
                    while i < len(s) and s[i].isdigit():
                        n = n * 10 + int(s[i]) 
                        i += 1

                else:
                    r.append(s[i]);
                    i += 1 

            return ''.join(r)
        i = 0
        return dfs(list(s))    
```

</details>
<BR>
