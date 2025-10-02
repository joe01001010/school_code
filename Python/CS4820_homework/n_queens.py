#!/usr/bin/env python
import math
import random


def main():
    solutions = {}
    solution, conflicts = simulated_annealing(4)
    solutions[4] = (solution, conflicts)
    print(f"n={4}: Solution = {solution}, Conflicts = {conflicts}")

    solutions = {}
    solution, conflicts = simulated_annealing(8)
    solutions[8] = (solution, conflicts)
    print(f"n={8}: Solution = {solution}, Conflicts = {conflicts}")


def check_conflicts(state):
    n = len(state)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts


def get_neighbor(state):
    n = len(state)
    new_state = state.copy()
    row = random.randint(0, n - 1)
    new_col = random.randint(0, n - 1)
    while new_col == state[row]:
        new_col = random.randint(0, n - 1)
    new_state[row] = new_col
    return new_state


def simulated_annealing(n, initial_temp=100.0, cooling_rate=0.95, min_temp=0.1):
    current_state = [random.randint(0, n - 1) for _ in range(n)]
    current_energy = check_conflicts(current_state)
    temp = initial_temp
    
    while temp > min_temp and current_energy > 0:
        neighbor = get_neighbor(current_state)
        neighbor_energy = check_conflicts(neighbor)
        delta_energy = neighbor_energy - current_energy
        
        if delta_energy < 0 or random.random() < math.exp(-delta_energy / temp):
            current_state = neighbor
            current_energy = neighbor_energy
        
        temp *= cooling_rate
    
    return current_state, current_energy


if __name__ == "__main__":
    main()