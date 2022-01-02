{: .no_toc}
# Stack
Practise here: [Leetcode](https://leetcode.com/list/?selectedList=9duv7mlj)

- TOC
{:toc}

### Basic Calculator

> Input: "(1+(4+5+2)-3)+(6+8)". BR
> Output: 23
> [Leetcode](https://leetcode.com/problems/basic-calculator/)

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

### Valid Parentheses

> Given a string containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.
> [Leetcode](https://leetcode.com/problems/valid-parentheses/)
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