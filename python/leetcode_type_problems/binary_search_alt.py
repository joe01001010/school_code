#!/usr/bin/env python3

def main():
    first_list = [False] * 24
    second_list = [True] * 2
    total_list = first_list + second_list
    left = 0
    right = len(total_list) - 1
    while left <= right:
        mid = (left + right) // 2
        if total_list[mid]:
            right = mid - 1
        else:
            left = mid + 1


if __name__ == "__main__":
    main()