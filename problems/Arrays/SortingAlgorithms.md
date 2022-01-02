{: .no_toc}
# Sorting Algorithms

- TOC
{:toc}

### Heap Sort

> Sort an array of integers, and find the maximum gap between any two in the sorted array.
> [Leetcode](https://leetcode.com/problems/maximum-gap/)

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:

    def maximumGap(self, num):
        if len(num) < 2:
            return 0

        num = self.heap_sort(num)
        res = 0
        for i in range(1, len(num)):
            res = max(num[i] - num[i - 1], res)
        return res

    def heap_sort(self, arr):
        def build_heap_at_i(arr, i, size):
            left = i * 2 + 1
            rigt = i * 2 + 2

            biggerChildren = [x for x in [left, rigt] if x <= size and arr[x]> arr[i] ]
            if len(biggerChildren) != 0:
                max_i = max(biggerChildren, key=lambda x: arr[x])

                arr[i], arr[max_i] = arr[max_i], arr[i]
                build_heap_at_i(arr, max_i, size)

        def build_heap(arr):
            size = len(arr)-1
            mid  = int(size/2)
            for i in range(mid,-1,-1):
                build_heap_at_i(arr, i, size)

        def heap_sort(arr):
            size = len(arr)-1
            for i in range(size, -1, -1):
                arr[0], arr[i] = arr[i], arr[0]
                size = size - 1
                build_heap_at_i(arr, 0, size)

        def print_heap(arr,i=0,d=0):
            if i not in range(0, len(arr)):
                return
            l = i*2+1
            r = i*2+2
            print_heap(arr,l,d+1)
            print("   " * d,arr[i])
            print_heap(arr,r,d+1)

        build_heap(arr)
        heap_sort(arr)
        return arr

```

</details>
<BR>


### Merge Sort

> Sort an array of integers, and find the maximum gap between any two in the sorted array.
> [Leetcode](https://leetcode.com/problems/maximum-gap/)

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:

    def maximumGap(self, num):
        if len(num) < 2:
            return 0

        num = self.radixSort(num)

        res = 0
        for i in range(1, len(num)):
            res = max(num[i] - num[i - 1], res)
        return res

    def radixSort(self, num):
        for i in range(31):
            onebucket = []
            zerobucket = []
            needle = 1 << i
            for j in range(len(num)):
                if num[j] & needle != 0:
                    onebucket.append(num[j])
                else:
                    zerobucket.append(num[j])
            num = []
            num += zerobucket
            num += onebucket
        return num
```

</details>
<BR>

### Quick Sort

> Sort an array of integers, and find the maximum gap between any two in the sorted array.
> [Leetcode](https://leetcode.com/problems/maximum-gap/)

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:

    def maximumGap(self, num):
        if len(num) < 2:
            return 0

        num = self.qsort(num)

        res = 0
        for i in range(1, len(num)):
            res = max(num[i] - num[i - 1], res)
        return res

    def qsort(self, L):
        if L == []:
            return []

        P = L[0]
        R = L[1:]

        return self.qsort([x for x in R if x< P])+ [P] + self.qsort([x for x in R if x>=P])
```

</details>
<BR>

### Radix Sort

> Sort an array of integers, and find the maximum gap between any two in the sorted array.
> [Leetcode](https://leetcode.com/problems/maximum-gap/)

<details><summary markdown="span">Let's see some code!</summary>

```python
```

</details>
<BR>
