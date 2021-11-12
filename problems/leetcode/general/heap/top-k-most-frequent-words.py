'''
Given a non-empty list of words, return the k most frequent elements.

Your answer should be sorted by frequency from highest to lowest. If two words have the same frequency, then the word with the lower alphabetical order comes first.

Example 1:
Input: ["i", "love", "leetcode", "i", "love", "coding"], k = 2
Output: ["i", "love"]
Explanation: "i" and "love" are the two most frequent words.
    Note that "i" comes before "love" due to a lower alphabetical order.
'''
class Solution:
    from typing import List
    from collections import Counter
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        heap = [(-val, key) for key,val in Counter(words).items()]
        heapq.heapify(heap)
        res = []
        while heap and k > 0:
            res.append(heapq.heappop(heap)[1])
            k -= 1
        return res
s = Solution()
arr = ["i", "love", "leetcode", "i", "love", "coding"]
print(s.topKFrequent(arr,2))