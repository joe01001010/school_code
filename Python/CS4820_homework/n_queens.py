#!/usr/bin/env python
import math, random, time

# You may need to do a pip install for these libraries but other than that ive been executing by cmd line
# Exmaple: python ./n_puzzle.py


def main():
    num_runs = 3
    start_test("Simulated Annealing", 4, num_runs)
    start_test("Simulated Annealing", 8, num_runs)
    start_test("Genetic Algorithm", 4, num_runs)
    start_test("Genetic Algorithm", 8, num_runs)


def start_test(test, n, runs):
    """
    This function will take the kind of test and the n value as arguments
    This function is only to ensure the program has a similarly formatted output per test
    This function has no return value
    """
    total_time  = []
    total_nodes = []
    for run in range(runs):
        print(f"Starting run {run + 1} for test {test} with N={n}")
        print("Starting state:")
        current_state = get_random_state(n)
        print_board(current_state)

        start_time = time.time()
        if test == "Simulated Annealing":
            solution, nodes_expanded = simulated_annealing(n, current_state)
        if test == "Genetic Algorithm":
            # this will get the random population generated and help in population
            population = initialize_population(n, 100)
            solution, nodes_expanded = genetic_algorithm(n, population)
        end_time = time.time()
        
        print("Solution Found:")
        print(f"Nodes expanded: {nodes_expanded}")
        print(f"Time: {end_time - start_time}")
        print_board(solution)
        print("=" * 100, end='\n\n')
        total_time.append(end_time - start_time)
        total_nodes.append(nodes_expanded)
    print(f"Average time for {runs} runs: {sum(total_time) / len(total_time)}")
    print(f"Average nodes for {runs} runs: {sum(total_nodes) / len(total_nodes)}")
    print()


def check_conflicts(state):
    """
    This function will take the current state as an argument and then check if any queens threaten eachother
    If they do it will increment the counter
    The function will then return the counter
    """
    n = len(state)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            # Check for row conflicts
            if state[i] == state[j]:
                conflicts += 1
            # Check for diagonal conflicts
            elif abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts


def random_neighbor(state):
    """
    This function takes the state as an argument
    This function will make a random new move and then return the new state
    """
    n = len(state)
    # Using .copy() so the potential nested data structure doesnt get modified
    new_state = state.copy()
    column_index = random.randint(0, n - 1)
    new_column = random.randint(0, n - 1)

    # Loop will ensure the random move is different than the intial configuration of the board
    while new_column == state[column_index]:
        new_column = random.randint(0, n - 1)
    new_state[column_index] = new_column
    return new_state


def get_random_state(n):
    return [random.randint(0,n-1) for i in range(n)]


def simulated_annealing(n, current_state, max_steps=99999, initial_temp=100, cooling_rate=0.99):
    """
    This takes 4 arguments
    n is the dimensions of the board and number of queens
    current_state is the randomly generated state of the board
    max_steps is the number of iterations to hit before stopping
    initial_temp is the randomness factor, controls how often it makes shitty moves
    coolintg_rate reduces the shitty move factor
    this returns the current_state and number of steps, and nodes_expanded
    """
    current_state = []
    for i in range(n):
        current_state.append(random.randint(0,n-1))

    # This will return the number of queens that are being threatened
    num_conflicts = check_conflicts(current_state)
    temp = initial_temp
    nodes_expanded = 0
    
    for step in range(max_steps):
        # Goal test to see if all the conflicts are gone
        if num_conflicts == 0:
            return current_state, nodes_expanded

        # Make small random change to configuration
        # calculate the number of conflicts after the random move
        # Get the differnce between the current and new number of conflicts
        neighbor = random_neighbor(current_state)
        neighbor_conflicts = check_conflicts(neighbor)
        difference = neighbor_conflicts - num_conflicts
        nodes_expanded += 1

        # If the neighbor is better take the neighbor's configuration
        # Also check if you want to accept with a probability based on the temp
        if difference < 0 or random.random() < math.exp(-difference / temp):
            current_state, num_conflicts = neighbor, neighbor_conflicts

        # lower the temperature so its less probabilistic
        temp *= cooling_rate

    return None, nodes_expanded


def print_board(state):
    """
    This function takes the board state and prints it
    This is solely for my visualization of the problem and solution
    This function doesnt return anything
    """
    for row in range(len(state)):
        line = ""
        for column in range(len(state)):
            line += "Q " if state[row] == column else ". "
        print(line)


def fitness(state):
    """
    Fitness is max possible non-attacking pairs minus actual conflicts
    This function takes the current state as an argument
    This function will rethr the max_pairs - number of conflicts
    """
    n = len(state)
    max_pairs = n * (n - 1) // 2
    return max_pairs - check_conflicts(state)


def initialize_population(n, size=100):
    """
    Create a population of random states
    This function takes 2 arguments
    n is the dimensions and number of queens
    size is the number of memebrs of the population to create
    This function will returna  list of random states in a list that is the length of size
    """
    return [get_random_state(n) for i in range(size)]


def select_parent(population, fitnesses):
    """
    Implements a roulette wheel selection
    This function takes two args
    population is the current population
    fitnesses is the list of fitness values
    This function will return the first naturally selected member of the population
    This function mimics the natural selection process in real life
    where only the 'fittest' members of the population will live on
    """
    total_fit = sum(fitnesses)
    pick = random.uniform(0, total_fit)
    current = 0
    for i, f in enumerate(fitnesses):
        current += f
        if current >= pick:
            return population[i]
    return population[-1]


def crossover(parent1, parent2):
    """
    Single point crossover between two parents
    This function takes two parents as arguments
    This function attemptes to combine the two parents into a child that can potentially be better than the parents
    This function will return the child
    """
    n = len(parent1)
    point = random.randint(1, n - 2)
    child = parent1[:point] + parent2[point:]
    return child


def mutate(state, mutation_rate=0.1):
    """
    Randomly change a queen's row with some probability
    This function takes two arguments
    state is the current configuration of the population
    mutation_rate is the randomness affect
    This function will return the new_state of the population
    """
    n = len(state)
    new_state = state.copy()
    if random.random() < mutation_rate:
        col = random.randint(0, n - 1)
        row = random.randint(0, n - 1)
        new_state[col] = row
    return new_state


def genetic_algorithm(n, population, max_generations=1000, mutation_rate=0.1):
    """
    This function takes 4 arguments
    n is the n value for queens and dimensions of the board
    max_generations is the number of iterations to run before returning
    mutation_rate is how often we intentionally mix things up so we can continue learning
    This function will return the solution and the number of generations
    """

    pop_size = len(population)
    nodes_expanded = 0
    for generation in range(max_generations):
        # Will create a list aligned with population that will show how well the population fits
        # High numbers is better in this scenario in regards to a solution
        fitness_list = [fitness(ind) for ind in population]
        nodes_expanded += len(population)

        # this checks for the best solution out of the previously created list
        best_idx = max(range(len(population)), key=lambda i: fitness_list[i])
        best_individual = population[best_idx]

        # This will check if there are conflicts in the best solution and if there are none it found a solution
        if check_conflicts(best_individual) == 0:
            return best_individual, nodes_expanded

        # This will select two new parents which will be used to make a new child
        # At the end of this it will make the queen go in a random row and create a new population
        new_population = []
        for i in range(pop_size):
            parent1 = select_parent(population, fitness_list)
            parent2 = select_parent(population, fitness_list)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population

    return None, nodes_expanded


if __name__ == "__main__":
    main()