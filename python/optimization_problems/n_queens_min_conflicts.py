#!/usr/bin/env python3
# You may need to do a pip install for the imports
# Example usage: python ./n_queens_min_conflicts.py
import random, time


def check_conflicts(state):
    """
    This function takes one argument
    state is the current configuration of the board
    This function returns the number of queens that are attacking each other
    """
    n = len(state)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts


def conflicts_for_queen(state, col, row):
    """
    This function takes three arguments
    state is the current configuration of the board
    col is the column we are working with
    row is the row we are working with
    This function will count how many conflicts a queen would have if placed in row and col
    """
    length = len(state)
    conflicts = 0
    for column in range(length):
        if column == col:
            continue
        if state[column] == row or abs(state[column] - row) == abs(column - col):
            conflicts += 1
    return conflicts


def get_conflicted_columns(state):
    """
    This function takes one argument
    state is the current configuration of the board
    This function will return a list of the columns that have queens attacking eachother
    """
    conflicted = []
    length = len(state)
    for column in range(length):
        if conflicts_for_queen(state, column, state[column]) > 0:
            conflicted.append(column)
    return conflicted


def min_conflicts(n, max_steps=1000000):
    """
    This function takes two arguments
    n is the number of diumensions and queens on the board (n in the n-queens problem)
    max_steps is the maximum number of steps to take before giving up (default to 1000000)
    This function will create a random configuration with a queen per row
    Then it will start iterating until it reaches the max amount of iterations allowed
    This function will check the conflicts and if it is 0 it will retunr the state and step
    else it will move queens to new columns to minimize congflicts
    If no solution is found within max steps it will return None and the max_steps
    """
    state = [random.randint(0, n - 1) for _ in range(n)]
    print("Starting Configuration:")
    print_board(state)

    for step in range(max_steps):
        total_conflicts = check_conflicts(state)
        if total_conflicts == 0:
            return state, step

        conflicted_cols = get_conflicted_columns(state)
        column = random.choice(conflicted_cols)

        min_conf = n + 1
        best_rows = []
        for row in range(n):
            conflicts = conflicts_for_queen(state, column, row)
            if conflicts < min_conf:
                min_conf = conflicts
                best_rows = [row]
            elif conflicts == min_conf:
                best_rows.append(row)

        state[column] = random.choice(best_rows)

    return None, max_steps


def print_board(state):
    """
    This function takes one argument
    state is the current configuration of the board
    This function will print the current configuraiton of the board to the screen
    This function doesnt return anything
    """
    if not state:
        print("No solution found.")
        return
    length = len(state)
    for row in range(length):
        line = ""
        for column in range(length):
            line += "Q " if state[column] == row else ". "
        print(line)
    print()


def solver(n, runs=5):
    """
    This function takes two arguments
    n is the dimensions of the board (n in the n-queens problem)
    runs is the number of runs to take for random configurations (defaults to 5)
    This function will print the number of steps taken and time taken to solve
    This function will print the average between the 5 runs as well
    """
    total_time = 0
    total_steps = 0
    for run in range(runs):
        print(f"Run {run + 1} for n = {n}")
        start_time = time.time()
        solution, steps = min_conflicts(n)
        elapsed = time.time() - start_time
        total_time += elapsed
        total_steps += steps
        if solution:
            print(f"Solved in {steps} steps ({elapsed:.4f} s)")
            print_board(solution)
        else:
            print(f"Failed after {steps} steps ({elapsed:.4f} s)")
        print("=" * 50)
    print(f"Average time: {total_time / runs:.4f} s")
    print(f"Average steps: {total_steps / runs:.1f}")
    print()


def main():
    """
    Takes no arguments
    main logic for program
    Calls the solver function sending the n variable for n-queens problem
    Returns nothing
    """
    solver(8)
    solver(16)
    solver(25)


if __name__ == "__main__":
    main()