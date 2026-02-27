#!/usr/bin/env python
# benchmark_optimization.py
# You might need to do pip installs for the imports 
# Execution: python ./benchmark_optimization.py
import numpy as np
import matplotlib.pyplot as plt
import time


class HiveMind:
    def __init__(self, dimensions, bounds):
        """
        Constructor for the HiveMind
        This constructor takes 2 arguments
        dimensions is the number of dimensions the hive will be working in
        bounds are the limits the hive needs to search within
        """
        self.position = np.random.uniform(bounds[0], bounds[1], dimensions)
        self.velocity = np.random.uniform(-1, 1, dimensions)
        self.best_position = self.position
        self.best_value = float('inf')


    def evaluate(self, function):
        """
        This function takes one argument
        function is the optimiztion function we are running against
        If the value produced byt he optimization function is better it will update
        else it will stay the same
        This function returns the value
        """
        value = function(self.position)
        if value < self.best_value:
            self.best_value = value
            self.best_position = self.position
        return value


    def update_velocity(self, global_best, inertia_weight, individual_hive_mind, swarm_hive_mind):
        """
        This function takes 4 arguments
        global_best is the best value the hive has found so far
        inertia_weight controls how muich the hive explores
        individual_hive_mind carries the wieght for how much individuals believe themselves
        swarm_hive_mind controls how much the individuals believe in the hive
        This function will ret random values and base those against the position of individuals
        This will take that value and put it agains the hive mind inertia
        this funciton will then update the velocity
        This function doesnt return anything
        """
        r1, r2 = np.random.rand(len(self.position)), np.random.rand(len(self.position))
        cognitive = individual_hive_mind * r1 * (self.best_position - self.position)
        social = swarm_hive_mind * r2 * (global_best - self.position)
        self.velocity = inertia_weight * self.velocity + cognitive + social


    def update_position(self, bounds):
        """
        This function takes one argument
        bounds is the tuple or list containing the parameters for the hive to search within
        This function doesnt return anything
        """
        self.position += self.velocity
        self.position = np.clip(self.position, bounds[0], bounds[1])


class TheHive:
    def __init__(self, function, dimensions, bounds, num_particles = 60, max_iterations = 200, inertia_weight=0.7, individual_hive_mind=1.5, swarm_hive_mind=1.5):
        """
        Constructor for TheHive
        This constructor takes 8 arguments
        This construction takes in the optimization function
        the dimensions to work in
        The bounds to search within
        num_particles or members of the hive, default to 30
        max_iterations, default to 200
        inertia_weight which controls the exploration for how the particles explore
        indicidual_hive_mind controls how much the particle believes itself
        swarm_hive_mind controls how much the particle believes in the hive
        """
        self.function = function
        self.dimensions = dimensions
        self.bounds = bounds
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        self.inertia_weight = inertia_weight
        self.individual_hive_mind = individual_hive_mind
        self.swarm_hive_mind = swarm_hive_mind

        self.hive_mind = [HiveMind(dimensions, bounds) for _ in range(num_particles)]
        self.global_best_position = np.zeros(dimensions)
        self.global_best_value = float('inf')
        self.convergence = []


    def optimize(self):
        """
        This function takes no arguments
        This function will loop over the max iterations
        This represents one hive mind or particle exploring the bounds of the dimensions
        This will see if the fitness is better than the global best and updat global best if so
        This function will track the convergence
        This function will also update velocitys
        This funtion returns 3 thigns
        This funtion will return the global best position in the form of a list or vector
        This function will return the global best value that was foudn by the hive
        This function will return the convergence
        """
        for iteration in range(self.max_iterations):
            for mind in self.hive_mind:
                fitness = mind.evaluate(self.function)
                if fitness < self.global_best_value:
                    self.global_best_value = fitness
                    self.global_best_position = mind.position

            self.convergence.append(self.global_best_value)

            for mind in self.hive_mind:
                mind.update_velocity(self.global_best_position, self.inertia_weight, self.individual_hive_mind, self.swarm_hive_mind)
                mind.update_position(self.bounds)

        return self.global_best_position, self.global_best_value, self.convergence


def rastrigin(X):
    """
    This function takes one argument
    X is a vector that will have the rastrigin value computed for
    This function returns a float
    """
    X = np.array(X, dtype=float)
    dimensions = X.size
    return 10 * dimensions + np.sum(X**2 - 10 * np.cos(2 * np.pi * X))


def rosenbrock(X):
    """
    This function takes one argument
    X is a list that gets converted into an array of floats in numpy
    This function will then run the rosenbrock function on the array
    This function will return a float
    """
    X = np.array(X, dtype=float)
    return np.sum(100 * (X[1:] - X[:-1]**2)**2 + (1 - X[:-1])**2)


def for_the_hive(runs, optimizer, optimizer_name, dimensions, bounds):
    """
    This function takes 5 arguments
    runs is the number of iteration to test on
    optimizer is the optimization function to use
    optimizer_name is a string representing the optimizer function
    dimensions is the number of dimensions for the hive to work in
    bounds is the limit of the search space for the hive
    This function will control the benchmark testing flow of the program and print to stdout
    this function doesnt return anything
    """
    print("=" * 10, end='')
    print(f" Running {optimizer_name} ", end='')
    print("=" * 10, end='\n\n')

    average_best_fitness = []
    average_best_value = []
    average_time = []
    all_convergences = []

    for run in range(1, runs + 1):
        print(f"{optimizer_name} run {run}/{runs}")
        hive_mind = TheHive(optimizer, dimensions, bounds)

        start_time = time.time()
        global_best_position, global_best_value, convergence = hive_mind.optimize()
        total_time = time.time() - start_time

        print(f"Global best position: {global_best_position}")
        print(f"Global best value: {global_best_value}")
        print(f"Time: {total_time}")
        print()

        average_best_fitness.append(global_best_position)
        average_best_value.append(global_best_value)
        average_time.append(total_time)
        all_convergences.append(convergence)
        
    print(f"Average best position: {np.mean(average_best_fitness, axis=0)}")
    print(f"Average best value: {np.mean(average_best_value)}")
    print(f"Average time: {np.mean(average_time)}", end='\n\n')

    print("=" * 10, end='')
    print(f" End {optimizer_name} ", end='')
    print("=" * 10, end='\n\n')

    plot_convergence(f"Convergence Curve: PSO on {optimizer_name}", f"PSO on {optimizer_name}", all_convergences)


def plot_convergence(plot_title, label, all_convergences):
    """
    This function takes 3 arguments
    plot_tiotle is the titel of the plot
    all_convergences is the collection of convergence thorughout optimization
    This funciton doesnt return anything
    This fucntion will visualy show the ocnvergence through optpimization for all runs
    """
    plt.figure(figsize = (8, 5))
    colors = plt.cm.viridis(np.linspace(0, 1, len(all_convergences)))
    for i, (conv, color) in enumerate(zip(all_convergences, colors)):
        plt.plot(conv, label=f"{label} {i+1}", color=color, linewidth=1.5, alpha=0.8)

    max_len = max(len(c) for c in all_convergences)
    padded = np.array([np.pad(c, (0, max_len - len(c)), 'edge') for c in all_convergences])
    mean_curve = np.mean(padded, axis=0)
    plt.plot(mean_curve, label="Mean Convergence", color="black", linewidth=2.5, linestyle="--")

    plt.title(plot_title)
    plt.xlabel("Iteration")
    plt.ylabel("Best Fitness Value")
    plt.yscale("log")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


def main():
    for_the_hive(3, rastrigin, 'Rastrigin', 2, (-10, 10))
    for_the_hive(3, rosenbrock, 'Rosenbrock', 2, (-10, 10))


if __name__ == '__main__':
    main()