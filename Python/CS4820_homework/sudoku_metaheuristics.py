#!/usr/bin/env python
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
    def __init__(self, board):
        self.board = board
        self.variables = [(row, column) for row in range(9) for column in range(9)]
        self.domains = {(row, column): set(range(1, 10)) if board[row][column] == 0 else {board[row][column]} for row in range(9) for column in range(9)}
        self.neighbors = self.build_neighbors()
        self.nodes_expanded = 0
        self.backtracks = 0


    def build_neighbors(self):
        neighbors = {}
        for row in range(9):
            for column in range(9):
                neighbor = set()
                for i in range(9):
                    if i != column:
                        neighbor.add((row, i))
                    if i != row:
                        neighbor.add((i, column))
                box_row, box_column = 3 * (row // 3), 3 * (column // 3)
                for i in range(box_row, box_row + 3):
                    for j in range(box_column, box_column + 3):
                        if (i, j) != (row, column):
                            neighbor.add((i, j))
                neighbors[(row, column)] = neighbor
        return neighbors


    def display_solution(self, assignment):
        solved = [[0]*9 for _ in range(9)]
        for (row, column), val in assignment.items():
            solved[row][column] = val

        for row in range(9):
            if row % 3 == 0 and row != 0:
                print("-" * 21)
            row_values = []
            for column in range(9):
                if column % 3 == 0 and column != 0:
                    row_values.append("|")
                val = solved[row][column]
                row_values.append(str(val))
            print(" ".join(row_values))


    def is_consistent(self, var, value, assignment):
        for number in self.neighbors[var]:
            if number in assignment and assignment[number] == value:
                return False
        return True


    def backtrack(self, assignment):
        self.nodes_expanded += 1
        if len(assignment) == 81:
            return assignment
        
        unassigned = [variable for variable in self.variables if variable not in assignment]
        variable = unassigned[0]

        for value in self.domains[variable]:
            if self.is_consistent(variable, value, assignment):
                assignment[variable] = value
                result = self.backtrack(assignment)
                if result:
                    return result
                self.backtracks += 1
                del assignment[variable]
        return None


    def __repr__(self):
        lines = []
        for row in range(9):
            if row % 3 == 0 and row != 0:
                lines.append("-" * 21)
            rows = []
            for column in range(9):
                if column % 3 == 0 and column != 0:
                    rows.append("|")
                val = self.board[row][column]
                rows.append(str(val) if val != 0 else ".")
            lines.append(" ".join(rows))
        return "\n".join(lines)


def main():
    sudoku_board = Sudoku(BOARD_EASY)
    print("Starting Board (Easy):")
    print(sudoku_board)
    start_time = time.time()
    solved_board = sudoku_board.backtrack({})
    print("Solved Board (Easy):")
    sudoku_board.display_solution(solved_board)
    print(f"Nodes Expanded: {sudoku_board.nodes_expanded}")
    print(f"Backtracks: {sudoku_board.backtracks}")
    print(f"Time: {time.time() - start_time:.4f} seconds")
    print("=" * 25, end='\n\n')

    sudoku_board = Sudoku(BOARD_MEDIUM)
    print("Starting Board (Medium):")
    print(sudoku_board)
    solved_board = sudoku_board.backtrack({})
    print("Solved Board (Medium):")
    sudoku_board.display_solution(solved_board)
    print(f"Nodes Expanded: {sudoku_board.nodes_expanded}")
    print(f"Backtracks: {sudoku_board.backtracks}")
    print(f"Time: {time.time() - start_time:.4f} seconds")
    print("=" * 25, end='\n\n')

    sudoku_board = Sudoku(BOARD_HARD)
    print("Starting Board (Hard):")
    print(sudoku_board)
    solved_board = sudoku_board.backtrack({})
    print("Solved Board (Hard):")
    sudoku_board.display_solution(solved_board)
    print(f"Nodes Expanded: {sudoku_board.nodes_expanded}")
    print(f"Backtracks: {sudoku_board.backtracks}")
    print(f"Time: {time.time() - start_time:.4f} seconds")
    print("=" * 25, end='\n\n')


if __name__ == '__main__':
    main()