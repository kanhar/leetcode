{: .no_toc}
# Bloom Filters
Practise here: [Leetcode]()

- TOC
{:toc}


### Sliding Median

> Given an n-ary tree, return the level order traversal of its nodes' values..
> [Leetcode](https://leetcode.com/problems/n-ary-tree-level-order-traversal/) <BR>

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def levelOrder(self, root: 'Node') -> List[List[int]]:
        def solve(node, d):
            if not node:
                return
            else:
                if d == 0:
                    res[d].append(node.val)
                    d += 1

                for child in node.children:
                    res[d].append(child.val)
                    solve(child, d + 1)

        res = collections.defaultdict(list)
        solve(root, 0)
        return res.values()
```

</details>
<BR>
