# 4Sum Problem - Optimal Approach

This is the optimal approach for the 4Sum problem, extending the 3Sum solution with an additional loop for the fourth element. The time complexity is O(n³), which cannot be further reduced for this problem.

## Solution Strategy

We sort the array first to place smaller numbers on the left and larger numbers on the right. The outer loop iterates from `i = 0` to `len(nums)-3`, reserving space for the remaining three elements. We skip duplicate values for `i` to avoid redundant computations.

For each `i`, the second loop runs from `j = i+1` to `len(nums)-2`, also skipping duplicates. Two pointers `l` and `r` are initialized: `l = j+1` and `r = len(nums)-1`.

In the while loop (`l < r`), we calculate the sum of `nums[i] + nums[j] + nums[l] + nums[r]`:

- If sum < target: increment `l` (move toward larger values)
- If sum > target: decrement `r` (move toward smaller values)
- If sum == target: add the quadruplet `[nums[i], nums[j], nums[l], nums[r]]` to results

## Handling Duplicates

After finding a valid quadruplet, we skip duplicates for both `l` and `r` using while loops:
- `while l < r and nums[l] == nums[l+1]: l += 1`
- `while l < r and nums[r] == nums[r-1]: r -= 1`

Then increment `l` and decrement `r` to continue searching.

## Code Reference

See `code.py` for the complete implementation.

## Technical Details

The algorithm uses four nested loops with optimization:
1. Outer loop `i` from 0 to `len(nums)-3` (leaves space for 3 more elements)
2. Inner loop `j` from `i+1` to `len(nums)-2` (leaves space for 2 more elements)
3. Two pointers `l = j+1` and `r = len(nums)-1` for the remaining two elements
4. Duplicate skipping at each level to avoid redundant computations