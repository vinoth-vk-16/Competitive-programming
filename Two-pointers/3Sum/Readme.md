# 3Sum Problem Solutions

## Brute Force Approaches

In the first two brute force approaches for the 3Sum problem, I used three nested loops. This leads to O(n³) time complexity, which is inefficient and not suitable for large inputs.

To avoid duplicate triplets in my results, I store each found triplet as a sorted tuple inside a set. This is because sets only allow hashable (immutable) types like tuples, not lists. Before adding a new triplet, I sort it and convert it to a tuple, then check if it is already in the set. If it is not present, I add it both to the set (to keep track) and to the final results.

Sorting each triplet before adding to the set ensures that combinations like [1, 1, 2] and [2, 1, 1] are treated the same, so duplicates are avoided.

In summary, the brute force method checks all possible triplets, ensures their sum is zero, and uses sorting plus a set to keep the results unique.

## Optimal Approach

The `code.py` file contains the most optimal approach for the 3Sum problem. First, we sort the array, which allows us to easily distinguish between larger and smaller numbers—after sorting, the right end contains the largest elements and the left end the smallest.

Next, we use a for loop that iterates up to n-2, since the last two positions are needed for the remaining elements of the triplet. To optimize further and avoid redundant computations, we skip duplicate values for the first element of the triplet (i). If the current value is the same as the previous, we continue to the next iteration.

For each i, we use two pointers: the left pointer (L), initialized to i+1, and the right pointer (R), initialized to the end of the list (n-1). We then compute the sum of the elements at i, L, and R. If the sum is less than zero, we increment the left pointer to increase the sum, since the array is sorted and moving right will lead to larger values. If the sum is greater than zero, we decrement the right pointer to decrease the sum. If the sum equals zero, we add the triplet to the result list.

To avoid duplicate triplets, instead of checking if the triplet is already in the result, we skip over duplicate values for the left and right pointers after a valid triplet is found. This way, we only consider unique triplets, efficiently preventing duplicates.

This approach efficiently finds all unique triplets that sum to zero without the need to explicitly check for duplicates in the results.

## Files

- `code.py` - Optimal two-pointer solution
- `Bruteforce-1.py` - First brute force implementation