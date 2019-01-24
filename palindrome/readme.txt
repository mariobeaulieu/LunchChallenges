This is not about real palindromes.
We try to find group of letters that appear 
in the same order when reading left to right
or right to left.

For example:

abcdabdababcd
should return:
(abcd)(ab)(d)(ab)(abcd)

We are looking for the minimum number of groups
so something like:

aabbaa

should return:
(aa)(bc)(aa)
and not 
(a)(a)(bc)(a)(a)

