#!/usr/bin/env python
import sympy

def main():
    aug_matrix = [
        [1, -1,  0,  0,  0,  0,  100],
        [0,  1, -1,  0,  0,  0,  -50],
        [0,  0,  1, -1,  0,  0,  120],
        [0,  0,  0,  1, -1,  0, -150],
        [0,  0,  0,  0,  1, -1,   80],
        [-1, 0,  0,  0,  0,  1, -100]
    ]

    print("Output linear equations:")
    print("=" * 25)
    """
    print_equations() expects an input of a matrix
    This function doesnt return anything
    This will only print the equations associated with the augmented matrix
    """
    print_equations(aug_matrix)
    print("", end='\n')

    """
    get_user_input() will take the augmented matrix as an argument and get a replacement value for some variable
    If the user inputs anything it will be validated as proper input
    Once the user inputs something the constraints will be returned as a dictionary
    The keys will be the variables and the value will be the value the user wants to input for that variable
    """
    constraints = get_user_input(aug_matrix)
    """
    general_solution() expects the augmented matrix as an argument and a dictionary of the constraints as the second argument
    This will perform a lot of data structure and object manipulation using the sympy library
    If there were no constraints it will print out the general form of the equations only and then end
    If there were constraints sent to the function it will attempt to solve for all the variables in the system
    If ther is an inconsistency or the system is unable to be solved based on the inputs
    It will output a message saying there is no solution based on the user input
    If there is a solution it will output the solution to the screen
    There is no return value
    """
    general_solution(aug_matrix, constraints)


def get_user_input(matrix):
    """
    Prompt user for input for specific variables
    Expects a matrix as input
    Will return constraints
    """
    constraints = dict()
    for i in range(1, len(matrix[0])):
        get_input = True
        while get_input:
            try:
                value = input(f"Enter a constraint for x{i} (Or skip 'ENTER'): ").strip()
                if value == "":
                    break
                constraints[f'x{i}'] = int(value)
                get_input = False
            except ValueError:
                print("Enter a valid integer or press ENTER to skip")

    print()
    return constraints


def print_equations(matrix):
    """
    Will display the system of linear equations if given the augmented matrix of the equations
    """
    for row in matrix:
        row_string = ""
        variable = "X"

        for index in range(len(row)):
            if index + 1 == len(row):
                row_string = f"{row_string} = {row[index]}"
                break # If its the last index in the row we print it and move on
            if row[index] == 0:
                continue # We dont care about printing variables if theyre zero in the augmented matrix

            coefficient = row[index]

            # This is for the first variable to be added to the row string
            if len(row_string) == 0:
                if coefficient > 0:
                    if coefficient == 1:
                        row_string = f"{variable}{index + 1}"
                    else:
                        row_string = f"{coefficient}{variable}{index + 1}"
                else:
                    if coefficient == -1:
                        row_string = f"-{variable}{index + 1}"
                    else:
                        row_string = f"{coefficient}{variable}{index + 1}"
                continue
            
            # This logic will separate the positives from negatives
            # This logic will also account for if the coefficient is not 1
            if coefficient > 0:
                if coefficient == 1:
                    row_string = f"{row_string} + X{index + 1}"
                else:
                    row_string = f"{row_string} + {coefficient}{variable}{index + 1}"
            else:
                if coefficient == -1:
                    row_string = f"{row_string} - X{index + 1}"
                else:
                    row_string = f"{row_string} - {abs(coefficient)}{variable}{index + 1}"
        print(row_string)


def general_solution(matrix, constraints):
    """
    Turn matrix into reduced row echelon form and find the general form of the equation
    Takes a matrix and constraints as arguments
    Does not return anything, only prints to screen
    """
    # Converting the matrix into a sympy matrix so the sympy library can perform operations on it
    sympy_matrix = sympy.Matrix(matrix)
    reduced_matrix, _ = sympy_matrix.rref() # This converts the matrix into reduced row echelon form
    
    print("RREF matrix:")
    print("=" * 25)
    sympy.pprint(reduced_matrix)
    print("", end='\n\n')

    # This is how sympy will be able to substitute and solve for my variables
    # I add the sympy symbol objects to a variables array for use later
    x1, x2, x3, x4, x5, x6 = sympy.symbols('x1 x2 x3 x4 x5 x6')
    variables = [x1, x2, x3, x4, x5, x6]

    # All the coefficients go into one array and the constants go into a separate array
    # linsolve will compute the general solution to the system returning a FiniteSet object
    A = sympy.Matrix([row[:-1] for row in matrix])
    b = sympy.Matrix([row[-1] for row in matrix])
    solution_set = sympy.linsolve((A, b), variables)
    # This pulls the tuple out of the solution set so I can play with it
    solution = next(iter(solution_set))

    print("General form solution:")
    print("=" * 25)
    solution_dict = dict()
    for variable, equation in zip(variables, solution):
        solution_dict[variable] = equation
        print(f"{variable} = {equation}")
    print()

    if constraints:
        # This turns all the constraints from the user input into sympy symbols for later calculations
        constraints    = {sympy.Symbol(k): v for k, v in constraints.items()}
        # This builds a list of sympy equalits objects of the general form created in the solution_dict
        # Then the constraint values from the user are appended onto the solution dict entries
        eqs            = [sympy.Eq(variable, expression) for variable, expression in solution_dict.items()]
        eqs           += [sympy.Eq(variable, value) for variable, value in constraints.items()]
        # This will solve the eqs list and the solution_dict.keys() tells the solve function from sympy what to solve for
        # In this case it will be x1, x2, etc...
        final_solution = sympy.solve(eqs, list(solution_dict.keys()), dict=True)

        if not final_solution:
            # This only executes if there is no solution based on the inputs from the user
            print(f"The constraints {constraints} cannot satisfy the system of equations")
        else:
            # If there is a solution it will print the solutions for the variables
            final_solution = final_solution[0]

            print("Solutions:")
            print("=" * 25)
            for variable, value in final_solution.items():
                print(f"{variable} = {value}")


if __name__ == "__main__":
    main()