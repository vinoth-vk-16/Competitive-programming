class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        seen=set()
        res=[]
        for i in range(0,len(nums)-2):
            for j in range(i+1,len(nums)):
                for k in range(j+1,len(nums)):
                    if nums[i]+nums[j]+nums[k]==0:
                        t=tuple(sorted([nums[i],nums[j],nums[k]]))
                        if t not in seen:
                            seen.add(t)
                            res.append(t)
        return res