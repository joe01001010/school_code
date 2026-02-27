#!/usr/bin/env python3

def binary_search(num_list, num_to_find):
    left = 0
    right = len(num_list) - 1
    while left <= right:
        mid = (left + right) // 2
        if num_list[mid] > num_to_find:
            right = mid - 1
        elif num_list[mid] < num_to_find:
            left = mid + 1
        else:
            return mid
    return -1


def main():
    num_to_find = 1001
    print("Target number:", num_to_find)
    num_list = list(range(1, 9999999, 2))

    index_for_num = binary_search(num_list, num_to_find)
    if index_for_num != -1:
        print(f"The index for {num_list[index_for_num]} is: {index_for_num}")
    else:
        print("The target number is not in the list")


if __name__ == '__main__':
    main()
