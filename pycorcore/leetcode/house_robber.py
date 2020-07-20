"""
You are a professional robber planning to rob houses along a street.
Each house has a certain amount of money stashed, the only constraint stopping you
from robbing each of them is that adjacent houses have security system connected and
it will automatically contact the police if two adjacent houses were broken into on the same night.

Given a list of non-negative integers representing the amount of money of each house,
determine the maximum amount of money you can rob tonight without alerting the police.
"""

# Thoughts:
# (1) Look at this as a dynamic programming problem.
# T(x) = max(x[0] + T(x[2:]), x[1] + T(x[3:])
# (2) Actually, recursion will work quite well since there are few overlapping problems.
# I can memoize to possibly make a little faster


def robber_recursive(house_money, start_idx=0, memo=None):

    if memo is None:
        memo = {
            len(house_money): 0,
            len(house_money)-1: house_money[-1]
        }

    if start_idx in memo:
        return memo[start_idx]

    if start_idx == (len(house_money) - 2):
        return max(house_money[-2:])

    return max(
        house_money[start_idx] + robber_recursive(house_money, start_idx=(start_idx+2), memo=memo),
        house_money[start_idx+1] + robber_recursive(house_money, start_idx=(start_idx+3), memo=memo)
    )


def robber_dynamic(house_money):

    # Initialize results for the end of the array
    cash = [0]*len(house_money)
    cash[-1] = house_money[-1]
    cash[-2] = max(house_money[-2:])

    # Work backwards and reference the results for the end.
    for idx in range(len(house_money)-3, -1, -1):
        cash[idx] = max(house_money[idx] + cash[idx+2], cash[idx+1])

    return cash[0]


def test_robber():

    #--- Memoized recursive solution
    # Test can skip 2
    max_cash = robber_recursive([0,1,2,3,4,5,6,7])
    assert max_cash == (1+3+5+7), "Max not achieved"

    # Test can skip 3
    max_cash = robber_recursive([0,1,4,0,1,5,0,1,6,0,1,7,1])
    assert max_cash == (4+5+6+7), "Max not achieved"

    # Test a mix
    max_cash = robber_recursive([2,15,11,1,6,8,7])
    assert max_cash == (15+6+7), "Max not achieved"

    #--- Dynamic solution
    # Test can skip 2
    max_cash = robber_dynamic([0,1,2,3,4,5,6,7])
    assert max_cash == (1+3+5+7), "Max not achieved"
        # Test can skip 3
    max_cash = robber_dynamic([0,1,4,0,1,5,0,1,6,0,1,7,1])
    assert max_cash == (4+5+6+7), "Max not achieved"

    # Test a mix
    max_cash = robber_dynamic([2,15,11,1,6,8,7])
    assert max_cash == (15+6+7), "Max not achieved"

if __name__ == "__main__":
    test_robber()


