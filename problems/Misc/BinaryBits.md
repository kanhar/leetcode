{: .no_toc}
# Binary Bit Manipulation
Practise here: [Leetcode](https://leetcode.com/list?selectedList=90xf0762)

- TOC
{:toc}
  
### [Binary Bit Count](https://leetcode.com/problems/number-of-1-bits/)

> Return the number of '1' bits in an unsigned integer. 

<details><summary markdown="span">Execute!</summary>

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


### [Reverse Bits of an integer](https://leetcode.com/problems/reverse-bits/)

> Reverse bits of a given 32 bits unsigned integer.

<details><summary markdown="span">Execute!</summary>

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
