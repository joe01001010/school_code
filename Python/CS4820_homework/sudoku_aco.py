#!/usr/bin/env python
# sudoku_aco.py
# You will potentially need to do a pip install for the imports
# Execution: python ./sudoku_aco.py
import numpy as np
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


def sudoku_fitness(board):
    """
    This function takes one argument
    board is the current configuration of the board
    This function will see how many conflicts exist in the board
    This function will return the numbe of conflicts
    """
    fitness = 0
    for row in board:
        fitness += 9 - len(set(row))
    for col in zip(*board):
        fitness += 9 - len(set(col))
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            block = [board[r][c] for r in range(br, br+3) for c in range(bc, bc+3)]
            fitness += 9 - len(set(block))
    return fitness


class SudokuACO:
    def __init__(self, board, n_ants=40, iterations=1000, evaporation=0.2, alpha=1.0, beta=2.0):
        """
        This is the initial constructor for SudokuACO
        This constructor takes 6 arguments
        board is the initial configuration of the board
        n_ants is the number of ants to use (default 40)
        iterations is the number of iterations to make during exploration (default 1000)
        evaportaion is the rate at which to evaporate
        alpha is how much impact the pheromone has
        beta is how much impact the heuristic has
        This constructor will also create pheromone which is a numpy array of ones for 3 dimensions
        Pheromone is 3 dimensions because of row, column and digit
        """
        self.board = np.array(board)
        self.fixed = (self.board != 0)
        self.pheromone = np.ones((9, 9, 9))
        self.n_ants = n_ants
        self.iterations = iterations
        self.evaporation = evaporation
        self.alpha = alpha
        self.beta = beta


    def heuristic(self, row, column, digit):
        """
        This fucntion takes three arguments
        row is the row we are working in
        column is the row we are working in
        digit is the digit to be placed in [row, column]
        This function will return the desirability in float form for placing digit in that space
        """
        """Desirability of placing digit d at (r, c)."""
        if digit in self.board[row, :] or digit in self.board[:, column]:
            return 0.1
        br, bc = 3 * (row // 3), 3 * (column // 3)
        block = self.board[br:br+3, bc:bc+3]
        return 0.1 if digit in block else 1.0


    def construct_solution(self):
        """
        This function takes no arguments
        This function will allow each any to build its own solution based on probability
        Each ant will start from the existing board and only fill in the empty cells
        This function will loop over all rows and columns and skip the cells that have values
        This function will initialize a probability and then compute pheromone
        This function will return a list called grid that is the solution for the ant
        """
        grid = self.board.copy()
        for row in range(9):
            for column in range(9):
                if self.fixed[row, column]:
                    continue
                probs = np.zeros(9)
                for number in range(1, 10):
                    pheromone_level = self.pheromone[row, column, number - 1] ** self.alpha
                    desirability = self.heuristic(row, column, number) ** self.beta
                    probs[number - 1] = pheromone_level * desirability
                probs /= probs.sum()
                grid[row, column] = np.random.choice(range(1, 10), p=probs)
        return grid


    def update_pheromones(self, solutions, fitnesses):
        """
        This function takes two arguments
        solutions is the list of sudoku cells that each ant has
        fitnesses is a list of fitness scores for the solutions
        This function will decay some of the pheromone
        This function will add new pheromones to good sudoku boards
        This function doesnt return anythin, it only updates variables in the class object
        """
        self.pheromone *= (1 - self.evaporation)
        for grid, fitness in zip(solutions, fitnesses):
            delta = 1 / (fitness + 1)
            for row in range(9):
                for column in range(9):
                    difference = int(grid[row, column]) - 1
                    self.pheromone[row, column, difference] += delta


    def optimize(self):
        """
        This function takes no arguments
        This function is the main ACO optimization logic
        This function will iterate over the predefined iterations in the class and call the constreuct_solution method
        This function will find the minimum fitness and update the best fitness and update the convergence
        This function will print the current fitness and iteration
        This function will return the best board, best fitness, and the convergence list
        If best_fitness hits 0 it means a solution was found and it will stop iterating early
        """
        best_board = None
        best_fitness = float('inf')
        convergence = []

        for it in range(self.iterations):
            ants = [self.construct_solution() for _ in range(self.n_ants)]
            fitnesses = np.array([sudoku_fitness(a) for a in ants])
            self.update_pheromones(ants, fitnesses)

            min_fit = fitnesses.min()
            if min_fit < best_fitness:
                best_fitness = min_fit
                best_board = ants[np.argmin(fitnesses)]

            convergence.append(best_fitness)
            print(f"Iteration {it+1}/{self.iterations}: best fitness = {best_fitness}")

            if best_fitness == 0:
                break

        return best_board, best_fitness, convergence


def run_trials(board, difficulty, n_trials=3):
    """
    This function takes three arguments
    board is the starting configuration to solve from
    difficulty is a string representing easy, medium, or hard
    n_trials is the number of times to test the solution
    This function will create a colony of ants and attempt to solve the sudoku
    This function will track the time and fitness
    This function will print the solved board if a solution is found
    This function will print the averages for best fitness and runtime
    This function will return the all_fitness and all_times variables for plotting if necessary
    """
    all_fitness = []
    all_times = []
    print(f"\n\nStarting {n_trials} tests for {difficulty}")
    for trial in range(1, n_trials + 1):
        print(f"\n===== ACO Sudoku Trial {trial}/{n_trials} =====")
        start = time.time()

        colony = SudokuACO(board)
        best_board, best_fit, convergence = colony.optimize()

        total_time = time.time() - start
        all_fitness.append(best_fit)
        all_times.append(total_time)

        print(f"Trial {trial} completed.")
        print(f"  Final best fitness (violations): {best_fit}")
        print(f"  Runtime: {total_time:.2f}s")

        if best_fit == 0:
            print(f"Found a solution:")
            print(best_board)
        else:
            print("No solution found")

    print("\n===== SUMMARY (3 TRIALS) =====")
    print(f"Average fitness: {np.mean(all_fitness):.2f}")
    print(f"Average time: {np.mean(all_times):.2f}s")

    return all_fitness, all_times


def main():
    run_trials(BOARD_EASY, "Easy", n_trials=3)
    #run_trials(BOARD_MEDIUM, "Medium", n_trials=3)
    #run_trials(BOARD_HARD, "Hard", n_trials=3)


if __name__ == "__main__":
    main()