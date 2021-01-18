'''
Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it is able to trap after raining.
'''
class Solution:
    #Very nicely explained here: https://www.youtube.com/watch?v=HmBbcDiJapY
    def trap(self, arr: List[int]) -> int:

        water = len(arr) * [0]
        for i in range(1,len(arr)):
            lmax = max(arr[:i])
            rmax = max(arr[i:])
            water[i] = max(water[i], min(lmax,rmax)-arr[i] )

        return sum(water)