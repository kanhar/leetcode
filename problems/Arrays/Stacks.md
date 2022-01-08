{: .no_toc}
# Stack
Practise here: [Leetcode](https://leetcode.com/list/?selectedList=9duv7mlj)

- TOC
{:toc}

### [Basic Calculator](https://leetcode.com/problems/basic-calculator/)

> Input: "(1+(4+5+2)-3)+(6+8)". BR
> Output: 23

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def calculate(self, s: str) -> int:
        res = num = 0
        sign = 1

        s = s + "+"
        stk = [sign]
        for a in s:
            if a.isdigit():
                num = num * 10 + (ord(a)-48)        # Create Number
            elif a in ['+', '-']:
                res += num * sign * stk[-1]         # +- Number ( & adjust for if in bracket sign)
                sign = 1 if a == '+' else -1        # Number complete
                num = 0
            elif a == '(':                          # Add previous sign to Stack. Reset sign
                stk.append(sign * stk[-1])
                sign = 1
            elif a == ')':                          # Add number and sign to result. Reset number.
                res += num * sign * stk[-1]
                num = 0
                stk.pop()
        return res

```

</details>
<BR>

### [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/)

> Given a string containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

<details><summary markdown="span">Let's see some code!</summary>

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
> [See also](https://kanhar.github.io/leetcode/problems/Misc/Regex.html#decode-string)

<details><summary markdown="span">Let's see some code!</summary>

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