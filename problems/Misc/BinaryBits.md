{: .no_toc}
# Binary Bit Manipulation
Practise here: [Leetcode](https://leetcode.com/list?selectedList=90xf0762)

- TOC
{:toc}
  
### Binary Bit Count

> Return the number of '1' bits in an unsigned integer. 
> [Leetcode](https://leetcode.com/problems/number-of-1-bits/)

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def hammingWeight(self, num: int) -> int:
        count = 0
        while num:
            if num & 1:
                count+=1
            num = num >> 1
        return count
```

</details>
<BR>


### Reverse Bits of an integer

> Reverse bits of a given 32 bits unsigned integer.
> [Leetcode](https://leetcode.com/problems/reverse-bits/)

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def reverseBits(self, n):
        res = 0
        pow = 31

        while n:
            tmp = (n&1) << pow
            res += tmp

            n = n >> 1
            pow -=1

        return res
```

</details>
<BR>
