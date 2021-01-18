'''

Revenue Milestones
We keep track of the revenue Facebook makes every day, and we want to know on what days Facebook hits certain revenue milestones. Given an array of the revenue on each day, and an array of milestones Facebook wants to reach, return an array containing the days on which Facebook reached every milestone.
Signature
int[] getMilestoneDays(int[] revenues, int[] milestones)
Input
revenues is a length-N array representing how much revenue FB made on each day (from day 1 to day N). milestones is a length-K array of total revenue milestones.
Output
Return a length-K array where K_i is the day on which FB first had milestones[i] total revenue.
Example
revenues = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
milestones = [100, 200, 500]
output = [4, 6, 10]
Explanation
On days 4, 5, and 6, FB has total revenue of $100, $150, and $210 respectively. Day 6 is the first time that FB has >= $200 of total revenue.
'''


def getMilestoneDays(revenues, milestones):
    if len(revenues) == 0:
        return []

    rev = [0] * len(revenues)
    rev[0] = revenues[0]
    for i in range(1,len(revenues) ):
        rev[i] = revenues[i] + rev[i-1]

    res = []
    idx = 0
    for m in milestones:
        while idx < len(rev) and rev[idx] < m:
            idx += 1
        res.append(idx+1)
        idx = 0
    return res

print([5, 4, 2, 3, 2] == getMilestoneDays([700, 800, 600, 400, 600, 700], [3100, 2200, 800, 2100, 1000] ))