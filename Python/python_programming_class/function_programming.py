import numpy as np


def incremenet_by_three(number):
    return number + 3


def main():
    list_one = [1,2,3,4,5]
    list_one_incremenented = list(map(incremenet_by_three, list_one))
    print(list_one_incremenented)

    list_one_incremented_lambda = list(map(lambda x: x+3, list_one_incremenented))
    print(list_one_incremented_lambda)

    list_one_incremented_lambda_numpy = np.array(list_one_incremented_lambda)
    list_one_incremented_lambda_numpy += 3
    print(list_one_incremented_lambda_numpy.tolist())

    cubed_even_numbers = tuple(filter(lambda y: y % 2 == 0, map(lambda x: x ** 3, list_one_incremented_lambda_numpy)))
    print(cubed_even_numbers)


if __name__ == '__main__':
    main()