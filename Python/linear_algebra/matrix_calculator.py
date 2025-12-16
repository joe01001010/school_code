#!/usr/bin/env python
import numpy as np


# Main logic of the program, will take the user's input and call the appropriate function
# If the user inputs 4 it will end the program
def main(run_program):
    while run_program:
        operation_to_perform = get_operation()

        if operation_to_perform == 1:
            addition()
        elif operation_to_perform == 2:
            subtraction()
        elif operation_to_perform == 3:
            scalar_multiplication()
        else:
            run_program = False


# This function will take integers for rows and columns and the matrix being created as a string to print out
# This function will iterate over all the rows that were send to this function
# If the user inputs a bad character for the value of the matrix it will reprompt.
# If the user doesnt input the correct number of elements per row it will reprompt
def build_matrix(rows, columns, matrix_being_created):
    print(f"{matrix_being_created}:")
    matrix = []
    print(f"Enter the elements of a {rows}x{columns} matrix:")
    for i in range(1, rows + 1):
        bad_input = True
        while bad_input:
            try:
                row = input(f"Row {i}: ")
                row = [int(item) for item in row.split()]
                if len(row) != columns:
                    print("Invalid input...")
                else:
                    matrix.append(row)
                    bad_input = False
            except (ValueError, TypeError):
                print("Invalid input...")
    return matrix


# This function returns two matrices always but will return an empty second matrix if only one is required
# The user will input in one line separated by a space the number of rows and columns and if they fail to do so it will reprompt
# Then the user's input will be split into rows and columns and then it will call build matrix function.
def get_matrix(one_matrix=False, get_input=True):
    while get_input:
        user_input = input("Enter rows and columns of the matrices: ")
        try:
            rows = int(user_input.split()[0])
            columns = int(user_input.split()[-1])
            get_input = False
        except ValueError:
            print("Invalid input...")
    # This function expects integers and a string as the arguments
    # This function will return a matrix of the size specified by the user.
    matrix1 = build_matrix(rows, columns, "Matrix 1")
    matrix2 = []
    if not one_matrix:
        # This function expects integers and a string as the arguments
        # This function will return a matrix of the size specified by the user.
        matrix2 = build_matrix(rows, columns, "Matrix 2")
        return matrix1, matrix2

    return matrix1


# Expects the user to input an integer and if the user fails to do so it will continue to prompt
# This function will return the scalar when it receives good input
def get_scalar(get_input=True):
    scalar = 0
    while get_input:
        try:
            scalar = int(input("Enter the scalar: "))
            get_input = False
        except ValueError:
            print("Invalid input...")
    return scalar
        

# Calls helper function to get two matrices and will add the matrices together displaying the output
def addition():
    # This function call will return 2 matrices but if only one is required it will return an empty array
    matrix1, matrix2 = get_matrix()
    numpy_matrix1 = np.array(matrix1)
    numpy_matrix2 = np.array(matrix2)
    print(numpy_matrix1)
    print(numpy_matrix2)
    numpy_matrix = numpy_matrix1 + numpy_matrix2

    # This loop is to conduct the manual addition of the matrices
    for row in range(len(matrix1)):
        for column in range(len(matrix1[row])):
            matrix1[row][column] += matrix2[row][column]
    print("Result:")
    print("Matrix:")
    print(matrix1)
    print("Numpy:")
    print(numpy_matrix)


# Calls helper function get get two matrices. The second matrix will be subtraced from the first matrix
def subtraction():
    # This function call will return 2 matrices but if only one is required it will return an empty array
    matrix1, matrix2 = get_matrix()
    numpy_matrix1 = np.array(matrix1)
    numpy_matrix2 = np.array(matrix2)
    numpy_matrix = numpy_matrix1 - numpy_matrix2
    # This loop is to conduct the manual subtraction of the matrices
    for row in range(len(matrix1)):
        for column in range(len(matrix1[row])):
            matrix1[row][column] -= matrix2[row][column]

    print("Result:")
    print("Matrix:")
    print(matrix1)
    print("Numpy:")
    print(numpy_matrix)


# Calls helper function to get matrix but will then do multiplication of array and matrix and print to demonstrate how they are similar
def scalar_multiplication():
    # This function call will return 2 matrices but if only one is required it will return an empty array
    matrix1 = get_matrix(one_matrix = True)
    scalar = get_scalar()
    numpy_array1 = np.array(matrix1)
    result_array = numpy_array1 * scalar
    # This loop is to conduct the manual multiplication of the matrices
    for row in range(len(matrix1)):
        for column in range(len(matrix1[row])):
            matrix1[row][column] *= scalar

    print("Result:")
    print("Matrix:")
    print(matrix1)
    print("Numpy:")
    print(result_array)


# The user is between 1 and 4 inclusive and if the user inputs anything other than 1, 2, 3, 4 it will continue to prompt for proper input
def get_operation():
    user_operation = 0
    while user_operation > 4 or user_operation < 1:
        try:
            user_operation = int(input("1. Addition\n2. Subtraction\n3. Scalar Multiplication\n4. Exit\nChoose an option: "))
        except ValueError:
            print("Invalid input...\n")
    return user_operation


# Call main function with True so the main loop logic will initiate
# This file also needs to be executable
if __name__ == '__main__':
    main(True)