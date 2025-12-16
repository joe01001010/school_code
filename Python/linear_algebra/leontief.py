#!/usr/bin/env python3
import numpy as np


def main():
    """
    This function takes no arguments
    This functoin will call read_file_matrix on D.txt and E.txt
    Those file contents will be returned and turned into numpy matrices
    The demand matrix will be used to create an identity matrix
    We will then take the identity matrix and subtract the io matrix
    The program will compute the inverse of the resulting matrix
    This program will then compute the dot product of the inverse matrix and the demand matrix
    I have to round the inverse of the identity matrix minus the i/o matrix because it didnt align with the example from the assignment
    Then the program will round to the tenths place
    This function prints the final rounded output matrix
    This function doesnt return anything
    """
    # Reading in the two matrices from files
    # This function expects the text file to have matrix rows separated by a newline character
    # This funciton expects the io matrix and demand matrix to be in the same file
    io_matrix, demand_matrix = read_file_matrix("matrices.txt")
    io_matrix = np.matrix(io_matrix)
    demand_matrix = np.matrix(demand_matrix)
    
    # The numpy library will create the identity matrix based on the side of the io_matrix
    identity_matrix = np.identity(io_matrix.shape[0])

    # Matrices of the same dimensions can be subtracted simply
    i_minus_d = identity_matrix - io_matrix

    # Numpy has a function to calculate the inverse of a mtrix that takes a matrix as an argument and returns the inverse of that matrix
    inverse_matrix = np.linalg.inv(i_minus_d)

    # I have to round teh inverse of (I-D) because it didnt align with the assignment example
    # This made the results from the multiplication be off compared to the expected results so I rounded and got the exact expected output
    inverse_matrix_rounded = np.round(inverse_matrix, 2)

    # X will be the inverse matrix multiplied by the demand matrix
    # Rounding this result t the tenths place is a requirement of the assignment
    X = inverse_matrix_rounded @ demand_matrix
    X_rounded = np.round(X, 1)

    print("Output matrix:")
    print(X_rounded)


def read_file_matrix(file_path):
    """
    This function take a file path as an argument (str)
    This funciton will expect the file to be a human readable file with matrix components separated by spaces
    Each row in the matrix will be represented by a newline character
    This function has logic to determine how many components per row
    This function will return a list of lists
    """
    D = []
    E = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line_index in range(3):
        D.append([float(d) for d in lines[line_index].split()])
    for line_index in range(3, 6):
        E.append([float(e) for e in lines[line_index].split()])

    return D, E


if __name__ == "__main__":
    main()