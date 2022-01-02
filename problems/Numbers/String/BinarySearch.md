{: .no_toc}
# Binary Bit Manipulation
Practise here: [Leetcode](https://leetcode.com/list?selectedList=90xf0762)

- TOC
{:toc}

### Binary Bit count

> Write a function that takes an unsigned integer and return the number of '1' bits it has (also known as the Hamming weight)
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

### Reverse Bits

> Suppose
> [Leetcode](https://leetcode.com/problems/reverse-bits/)

<details><summary markdown="span">Let's see some code!</summary>

```python

```

</details>
<BR>