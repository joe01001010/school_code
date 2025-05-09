import numpy as np
from functools import reduce


def incremenet_by_three(number):
    return number + 3


def main():
    list_one = [1,2,3,4,5]
    print("Initial list:", list_one, end='\n\n')

    list_one_incremenented = list(map(incremenet_by_three, list_one))
    print("Incremeneted by three using map:", list_one_incremenented, end='\n\n')

    list_one_incremented_lambda = list(map(lambda x: x+3, list_one_incremenented))
    print("Incremented by three using map with lambda:", list_one_incremented_lambda, end='\n\n')

    list_one_incremented_lambda_numpy = np.array(list_one_incremented_lambda)
    list_one_incremented_lambda_numpy += 3
    print("Incremented list using numpy:", list_one_incremented_lambda_numpy.tolist(), end='\n\n')

    other_list = [100,200,300]
    print("Introduce a new list to add to incremented list using numpy:", other_list, end='\n\n')

    add_two_lists = list(map(lambda x,y: x + y, list_one_incremented_lambda_numpy, other_list ))
    print("Element summation of cubed list and new list:", add_two_lists, end='\n\n')

    sum_of_cubed_even_numbers = reduce(lambda x,y: x + y, filter(lambda y: y % 2 == 0, map(lambda x: x ** 3, list_one_incremented_lambda_numpy)))
    print("Cube each element of list and only return even:", sum_of_cubed_even_numbers, end='\n\n')


if __name__ == '__main__':
    main()