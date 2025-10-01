#!/usr/bin/env python
import random, time
from collections import deque

def main():
    goal = (0,1,2,3,4,5,6,7,8)
    start = get_random_start(goal)
    start_test('Breadth-First Search', start, goal)
    start_test('Depth-First Search', start, goal)
    start_test('Iterative Deepening Search', start, goal)
    start_test('Bidirectional Search', start, goal)
    
    goal = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
    start = get_random_start(goal)
    start_test('Breadth-First Search', start, goal)
    start_test('Depth-First Search', start, goal)
    start_test('Iterative Deepening Search', start, goal)
    start_test('Bidirectional Search', start, goal)


def start_test(test, start, goal, num_tests = 3):
    for test_num in range(num_tests):
        print(f"Starting test number {test_num + 1} for {test} with {len(goal)} elements")
        print("=" * 100)
        print(f"Starting configuration: {start}")
        start_time = time.time()

        if test == 'Breadth-First Search':
            path_found = bfs(start, goal)
        elif test == 'Depth-First Search':
            path_found = dfs(start, goal)
        elif test == 'Iterative Deepening Search':
            path_found = ids(start, goal)
        elif test == 'Bidirectional Search':
            path_found = bds(start, goal)
        else:
            print("No test for your thingy")
            return None

        if path_found:
            print(f"Found a sneaky little path of length: {len(path_found)}")
        print(f"Time for {test}: {time.time() - start_time}", end='\n\n')


def get_random_start(goal):
    # Returns a random tuple of numbers from 0-n where 0 represents the blank space
    # n represents the highest number in the goal state
    numbers = list(range(max(goal) + 1))
    random.shuffle(numbers)
    return tuple(numbers)


def bfs(start, goal):
    queue = deque([start])
    visited = set([start])
    parent = {start: None}
    
    while queue:
        state = queue.popleft()
        if state == goal:
            return reconstruct_path(parent, state)
        
        for neighbor in get_surrounding_tiles(state):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = state
                queue.append(neighbor)
    return None


def dls(state, goal, depth, parent, visited):
    if state == goal:
        return True
    if depth == 0:
        return False
    
    for neighbor in get_surrounding_tiles(state):
        if neighbor not in visited:
            visited.add(neighbor)
            parent[neighbor] = state
            if dls(neighbor, goal, depth-1, parent, visited):
                return True
    return False


def ids(start, goal, max_depth=50):
    for depth in range(max_depth):
        parent = {start: None}
        visited = set([start])
        if dls(start, goal, depth, parent, visited):
            return reconstruct_path(parent, goal)
    return None


def bds(start, goal):
    front_start = {start: None}
    front_goal = {goal: None}
    queue_start, queue_goal = deque([start]), deque([goal])
    visited_start, visited_goal = set([start]), set([goal])
    
    while queue_start and queue_goal:
        state = queue_start.popleft()
        for neighbor in get_surrounding_tiles(state):
            if neighbor not in visited_start:
                visited_start.add(neighbor)
                front_start[neighbor] = state
                queue_start.append(neighbor)
                if neighbor in visited_goal:
                    return merge_paths(front_start, front_goal, neighbor)
        
        state = queue_goal.popleft()
        for neighbor in get_surrounding_tiles(state):
            if neighbor not in visited_goal:
                visited_goal.add(neighbor)
                front_goal[neighbor] = state
                queue_goal.append(neighbor)
                if neighbor in visited_start:
                    return merge_paths(front_start, front_goal, neighbor)
    return None


def dfs(start, goal, max_depth=1000):
    stack = [(start, [start])]
    visited = set([start])
    nodes_expanded = 0
    
    while stack:
        state, path = stack.pop()
        nodes_expanded += 1
        
        if state == goal:
            print(f"DFS nodes expanded: {nodes_expanded}")
            return path
        
        if len(path) > max_depth:
            continue
            
        for neighbor in get_surrounding_tiles(state):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))
    
    return None


def merge_paths(front_start, front_goal, meet):
    path1 = reconstruct_path(front_start, meet)
    path2 = reconstruct_path(front_goal, meet)[::-1]
    return path1 + path2[1:]


def get_surrounding_tiles(state):
    neighbors = []
    size = int(len(state) ** 0.5)
    zero_index = state.index(0)
    row, col = divmod(zero_index, size)
    
    moves = []
    if row > 0: 
        moves.append((-1, 0))
    if row < size-1:
        moves.append((1, 0))
    if col > 0:
        moves.append((0, -1))
    if col < size-1:
        moves.append((0, 1))
    
    for dr, dc in moves:
        r, c = row + dr, col + dc
        new_index = r * size + c
        new_state = list(state)
        new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
        neighbors.append(tuple(new_state))
    
    return neighbors


def reconstruct_path(parent, state):
    path = []
    while state is not None:
        path.append(state)
        state = parent[state]
    return path[::-1]



if __name__ == '__main__':
    main()