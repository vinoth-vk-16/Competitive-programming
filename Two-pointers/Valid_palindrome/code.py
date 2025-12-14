class Solution:
    def isPalindrome(self, s: str) -> bool:
        s1=""
        for val in reversed(s):
            if val.isalnum():
                s1+=val
        s1=s1.lower()
        s2=s1[::-1]
        return s1==s2
        