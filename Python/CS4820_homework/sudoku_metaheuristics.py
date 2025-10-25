#!/usr/bin/env python
# sudoku_metaheuristics.py
# You will potentially need to do a pip install for the imports
# Execution: python ./sudoku_metaheuristics.py
import time


BOARD_EASY = [
    [0,0,0,2,6,0,7,0,1],
    [6,8,0,0,7,0,0,9,0],
    [1,9,0,0,0,4,5,0,0],
    [8,2,0,1,0,0,0,4,0],
    [0,0,4,6,0,2,9,0,0],
    [0,5,0,0,0,3,0,2,8],
    [0,0,9,3,0,0,0,7,4],
    [0,4,0,0,5,0,0,3,6],
    [7,0,3,0,1,8,0,0,0]
]
BOARD_MEDIUM = [
    [0,0,0,0,0,0,0,1,2],
    [0,0,0,0,0,0,0,0,0],
    [0,3,0,0,0,5,4,0,0],
    [0,0,0,0,0,0,1,0,0],
    [0,0,1,0,0,0,0,0,0],
    [0,0,0,3,0,0,0,0,0],
    [0,4,0,2,0,0,0,0,0],
    [9,0,0,0,0,0,0,0,0],
    [0,0,7,0,0,0,3,0,0]
]
BOARD_HARD = [
    [8,0,0,0,0,0,0,0,0],
    [0,0,3,6,0,0,0,0,0],
    [0,7,0,0,9,0,2,0,0],
    [0,5,0,0,0,7,0,0,0],
    [0,0,0,0,4,5,7,0,0],
    [0,0,0,1,0,0,0,3,0],
    [0,0,1,0,0,0,0,6,8],
    [0,0,8,5,0,0,0,1,0],
    [0,9,0,0,0,0,4,0,0]
]

class Sudoku:
    """
    This class is designed for taking in a board of a 9x9 sudoku puzzle
    This funciton will use metaheuristics to solve the puzzle and report the nodes expanded, time, number of backtracks
    """
    def __init__(self, board):
        """
        Initial constructor for the class
        This takes the board as an argument
        board is a list of lists with randomly generated values
        """
        self.board = board
        self.variables = [(r, c) for r in range(9) for c in range(9) if board[r][c] == 0]
        self.neighbors = self.build_neighbors()
        self.domains = {}
        for r, c in self.variables:
            used = self.row_vals(r) | self.col_vals(c) | self.box_vals(r, c)
            self.domains[(r, c)] = {v for v in range(1, 10) if v not in used}
        self.nodes_expanded = 0
        self.backtracks = 0


    def row_vals(self, row):
        """
        This function takes row as an argument
        the column represents the rows we are working in 
        This function will return a dict of values in the row
        """
        return {self.board[row][j] for j in range(9) if self.board[row][j] != 0}


    def col_vals(self, column):
        """
        This function takes column as an argument
        the column represents the columns we are working in 
        This cuntion will return a dict of values in the column
        """
        return {self.board[i][column] for i in range(9) if self.board[i][column] != 0}


    def box_vals(self, row, column):
        """
        This funciton takes two arguments
        row is the row we are working with
        column is the column we are working with
        this is the coordinates of what we are working with
        This function returns a set of the values
        """
        box_row, box_column = 3 * (row // 3), 3 * (column // 3)
        values = set()
        for i in range(box_row, box_row + 3):
            for j in range(box_column, box_column + 3):
                value = self.board[i][j]
                if value != 0:
                    values.add(value)
        return values


    def build_neighbors(self):
        """
        This function takes no arguments
        This funciton is what implements the constraints of this problem
        This function returns a dict of lists of tuples that is the neighbors
        """
        neighbors_final = {}
        for row in range(9):
            for column in range(9):
                neighbors = set()
                for i in range(9):
                    if i != column: neighbors.add((row, i))
                    if i != row: neighbors.add((i, column))
                box_row, box_column = 3 * (row // 3), 3 * (column // 3)
                for i in range(box_row, box_row + 3):
                    for j in range(box_column, box_column + 3):
                        if (i, j) != (row, column):
                            neighbors.add((i, j))
                neighbors_final[(row, column)] = neighbors
        return neighbors_final


    def display_solution(self, assignment):
        """
        This function takes one argument
        assignment is the current configuration of the solution, should be the completed puzzle
        This function doesnt return anything
        """
        solved = [row[:] for row in self.board]
        for (r, c), v in assignment.items():
            solved[r][c] = v
        for r in range(9):
            if r % 3 == 0 and r != 0:
                print("-" * 21)
            row = []
            for c in range(9):
                if c % 3 == 0 and c != 0:
                    row.append("|")
                row.append(str(solved[r][c]))
            print(" ".join(row))


    def __repr__(self):
        """
        This funciton takes no arguments
        This is just a sanity check function that prints the board
        This function returns a string represetning the board
        """
        lines = []
        for r in range(9):
            if r % 3 == 0 and r != 0:
                lines.append("-" * 21)
            row = []
            for c in range(9):
                if c % 3 == 0 and c != 0:
                    row.append("|")
                val = self.board[r][c]
                row.append(str(val) if val != 0 else ".")
            lines.append(" ".join(row))
        return "\n".join(lines)


    def is_consistent(self, var, value, assignment):
        """
        This function takes 3 arguments
        var is the cell im about to assign a value to
        value is the value I want to put in that cell
        assignment is the current configuraiton of my solution
        This function returns a boolean value, false if it cant assign this value here, else true
        """
        for neighbor in self.neighbors[var]:
            if neighbor in assignment and assignment[neighbor] == value:
                return False
        return True


    def select_unassigned_variable(self, assignment):
        """
        This funciton takes one argument
        Assignment is the current partial solution of the sudoku puzzle
        This function will attempt to find the most likely option to cause a backtrack sooner
        This function returns the potential solution that has the fewest possible solutions
        """
        unassigned = [variable for variable in self.variables if variable not in assignment]
        min_domain = 10
        candidates = []
        for variable in unassigned:
            domain = len(self.domains[variable])
            if domain < min_domain:
                min_domain = domain
                candidates = [variable]
            elif domain == min_domain:
                candidates.append(variable)
        if len(candidates) == 1:
            return candidates[0]
        return max(candidates, key=lambda v: sum(1 for neighbor in self.neighbors[v] if neighbor in unassigned))


    def order_domain_values(self, var, assignment):
        """
        This function takes two arguments
        var is a row column pair that I want to assign a number to
        assignment is the current partiabl solution
        This funciton will return the sorted domain variables with conflicts it has
        """
        unassigned_neighbors = [neighbor for neighbor in self.neighbors[var] if neighbor in self.variables and neighbor not in assignment]
        neighbor_domains = [self.domains[neighbor] for neighbor in unassigned_neighbors]
        def conflicts(val):
            return sum(val in domain for domain in neighbor_domains)
        return sorted(self.domains[var], key=conflicts)


    def forward_check(self, var, value, assignment):
        """
        This function takes 3 arguments
        var is the current variable or cell we are working with
        value is the number 1-9 that needs to be removed from the domains of the neighbors
        assignment is the current state of the problem
        This function will return none if the neighbors domain is empty
        Else this function will return a list of tuples with the neighbor and the removed value
        """
        removed = []
        for neighbor in self.neighbors[var]:
            if neighbor in self.variables and neighbor not in assignment:
                if value in self.domains[neighbor]:
                    self.domains[neighbor].remove(value)
                    removed.append((neighbor, value))
                    if not self.domains[neighbor]:
                        for (variable, value) in removed:
                            self.domains[variable].add(value)
                        return None
        return removed


    def restore(self, removed):
        """
        This function takes one argument
        removed is the list of tuples that was removed
        This function will add the value back into the domain
        This function doesnt return anything
        """
        for (variable, value) in removed:
            self.domains[variable].add(value)


    def backtrack(self, assignment):
        """
        This funciton is the main logic for backtracking
        This function takes one argument
        The assignmnet argument is for the current partial solution of the board
        The first imporovement that was implemented was forward checking
        This function will return the result or None as it recurses on itself.
        This function has a base case if the number of variables is the same as the length of assignmnet
        """
        self.nodes_expanded += 1
        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                removed = self.forward_check(var, value, assignment)
                if removed is not None:
                    result = self.backtrack(assignment)
                    if result:
                        return result
                if removed is not None:
                    self.restore(removed)
                self.backtracks += 1
                del assignment[var]
        return None


def solver(board_to_solve, difficulty):
    """
    This function takes two arguments
    The first is a starting configuration of a sudoku board to solve
    The second is the difficulty as a string
    This function doesnt return anything
    """
    starting_board = Sudoku(board_to_solve)
    print(f"Starting Board ({difficulty}):")
    print(starting_board)
    start_time = time.time()
    solved_board = starting_board.backtrack({})
    elapsed = time.time() - start_time
    print(f"Solved Board ({difficulty}):")
    starting_board.display_solution(solved_board)
    print(f"Nodes Expanded: {starting_board.nodes_expanded}")
    print(f"Backtracks: {starting_board.backtracks}")
    print(f"Time: {elapsed:.4f} seconds")
    print("=" * 25, end="\n\n")


def main():
    """
    This function takes no arguments and doesnt return anything
    This function controls the logic for the program and calls the solver function with the board to solve
    """
    solver(BOARD_EASY, "Easy")
    solver(BOARD_MEDIUM, "Medium")
    solver(BOARD_HARD, "Hard")

if __name__ == "__main__":
    main()
