#!/usr/bin/env python3

import sys
sys.setrecursionlimit(1000000)

def return_fibonacci_number(number, memo={}):
    if number in memo:
        return memo[number]

    if number <=0:
        return 0
    
    if number <= 2:
        return 1
    
    result = return_fibonacci_number(number-1, memo) + return_fibonacci_number(number-2, memo)
    memo[number] = result
    return result



def main():
    print(return_fibonacci_number(10000))


if __name__ == "__main__":
    main()