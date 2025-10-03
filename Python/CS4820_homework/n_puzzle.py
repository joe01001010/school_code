#!/usr/bin/env python
import random, time, heapq
from collections import deque

def main():
    goal = (0,1,2,3,4,5,6,7,8)
    start_test('A* Manhattan', goal)
    start_test('A* Misplaced', goal)
    start_test('Bidirectional Search', goal)
    start_test('Breadth-First Search', goal)
    start_test('Iterative Deepening Search', goal)
    start_test('Depth-First Search', goal)
    
    goal = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
    start_test('A* Manhattan', goal)
    # start_test('A* Misplaced', goal)
    # start_test('Bidirectional Search', goal)
    # start_test('Breadth-First Search', goal)
    # start_test('Iterative Deepening Search', goal)
    # start_test('Depth-First Search', goal)


def start_test(test, goal, num_tests = 3):
    """
    Formatting function for consistent output for all tests being run
    Takes 3 arguments
    test is the kind of test being run as a string
    goal is the desired state of the board as a tuple
    num_tests is an int identifying the number of tests to run for each search algorithm, defaults to three
    This function doesnt return anything
    """
    average_times = []
    average_nodes_expanded = []

    for test_num in range(num_tests):
        print(f"{test} test number {test_num+ 1} with {len(goal)} elements")
        start = get_random_start(goal)
        print(f"Starting configuration: {start}")
        start_time = time.time()

        if test == 'Breadth-First Search':
            path_found, nodes_expanded = bfs(start, goal)
        elif test == 'Depth-First Search':
            path_found, nodes_expanded = dfs(start, goal)
        elif test == 'Iterative Deepening Search':
            path_found, nodes_expanded = ids(start, goal)
        elif test == 'Bidirectional Search':
            path_found, nodes_expanded = bds(start, goal)
        elif test == 'A* Manhattan':
            path_found, nodes_expanded = astar(start, goal, 'manhattan')
        elif test == 'A* Misplaced':
            path_found, nodes_expanded = astar(start, goal, 'misplaced')

        print(f"Stats for run {test_num + 1}:")
        if path_found:
            print(f"Path Length: {len(path_found)}")
            print(f"Depth: {len(path_found) - 1}")
        else:
            print("No path found")
        print(f"Time for {test}: {time.time() - start_time}")
        print(f"Expanded nodes: {nodes_expanded}", end='\n\n')
        average_times.append(time.time() - start_time)
        average_nodes_expanded.append(nodes_expanded)
    print(f"Average nodes expanded for {num_tests} {test} runs: {sum(average_nodes_expanded) / len(average_nodes_expanded)}")
    print(f"Average time for {num_tests} {test} runs: {sum(average_times) / len(average_times)}")
    print("=" * 100, end='\n\n')



def get_random_start(goal):
    # Returns a random tuple of numbers from 0-n where 0 represents the blank space
    # n represents the highest number in the goal state
    numbers = list(range(max(goal) + 1))
    random.shuffle(numbers)
    return tuple(numbers)


def bfs(start, goal):
    """
    Classic breadth first search
    takes 2 arguments
    start is the initial configuration state of the board
    goal is the desired configuration state of the board
    This function returns the path and number of nodes expanded if a path is found
    If no path is found it will return None and the number of nodes expanded
    """
    # BFS uses a queue for searching
    queue = deque([start])
    visited = set([start])
    # Initialize the dictionary for mapping if the goal state is found
    parent = {start: None}
    nodes_expanded = 0
    
    while queue:
        # Start searching from the front of the queue and increment the nodes_expanded by 1
        state = queue.popleft()
        nodes_expanded += 1
        if state == goal:
            return reconstruct_path(parent, state), nodes_expanded
        
        for neighbor in get_surrounding_tiles(state):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = state
                queue.append(neighbor)
    return None, nodes_expanded


def dls(state, goal, depth, parent, visited, nodes_expanded):
    """
    Depth limited search, called by iterative depth search
    takes 6 arguments
    state is the current configureation of the board
    goal is the desired configuration of the board
    parent is the dictionary to reconstruct if the goal is found and to modify for future searches
    visited set is to ensure we dont evaluate an already visited state of the board
    nodes_expanded is to keep track of how many nodes we visited, this is passed as a pointer so recursive calls can increment it
    This will return a boolean value if the goal is found it will return true else false
    """
    nodes_expanded[0] += 1
    if state == goal:
        return True
    if depth == 0:
        return False
    
    for neighbor in get_surrounding_tiles(state):
        if neighbor not in visited:
            visited.add(neighbor)
            parent[neighbor] = state
            if dls(neighbor, goal, depth-1, parent, visited, nodes_expanded):
                return True
    return False


def ids(start, goal, max_depth=100):
    """
    Iterative deepending search
    Takes 3 arguments 
    start is the initial state of the board
    goal is the desired state of the board
    max_depth is the number of allowed searches depth wise
    This will return a path and number of nodes expanded if a path is found
    If no path is found it will return None and the total number of nodes expanded
    """
    total_nodes_expanded = 0
    # Each loop will increase how deep the IDS can go
    for depth in range(max_depth):
        parent = {start: None}
        visited = set([start])
        nodes_expanded = [0]
        # DLS is basicallf DFS except it has a depth limit
        # returns a boolean value
        if dls(start, goal, depth, parent, visited, nodes_expanded):
            total_nodes_expanded += nodes_expanded[0]
            return reconstruct_path(parent, goal), total_nodes_expanded
    return None, total_nodes_expanded


def bds(start, goal):
    """
    Bi-directional search
    takes two arguments start and goal
    start being the current configuration of the board
    goal being the desired and configuration of the board
    This function will attempt to work the paths simultaneously towards eachother and meet in the middle
    This function will reutrn the path and number of nodes expanded
    If no path is found it will return None and number of nodes expanded
    """
    front_start = {start: None}
    front_goal = {goal: None}
    # Creates two queues like BFS so they can start searching from both ends towards eachother
    queue_start, queue_goal = deque([start]), deque([goal])
    visited_start, visited_goal = set([start]), set([goal])
    nodes_expanded = 0
    
    # Runs as long as they both have options in the queue
    while queue_start and queue_goal:
        # Start searching from the initial configuration state of the board
        state = queue_start.popleft()
        nodes_expanded += 1
        for neighbor in get_surrounding_tiles(state):
            if neighbor not in visited_start:
                visited_start.add(neighbor)
                front_start[neighbor] = state
                queue_start.append(neighbor)
                if neighbor in visited_goal:
                    return merge_paths(front_start, front_goal, neighbor), nodes_expanded
        
        # Start searching from the goal state back towards the initial configuration state
        state = queue_goal.popleft()
        nodes_expanded += 1

        for neighbor in get_surrounding_tiles(state):
            if neighbor not in visited_goal:
                visited_goal.add(neighbor)
                front_goal[neighbor] = state
                queue_goal.append(neighbor)
                if neighbor in visited_start:
                    return merge_paths(front_start, front_goal, neighbor), nodes_expanded
    return None, nodes_expanded


def dfs(start, goal, max_depth=1000):
    f"""
    depth first search algorithm takes 3 arguments
    start being the current configuration of the puzzle
    goal being the end state of the puzzle
    max_depth to prevent infinite loops and adhere to the python standard limit of 1000
    Python can recurse more than 1000 if necessary but I need to explicitly tell it to allow that
    Will return a found path and number of nodes expanded
    If no path is foudn it will return None and the number of nodes expanded
    """
    # Make the stack for dfs and set visited to the current configuration of the board
    stack = [(start, [start])]
    visited = set([start])
    nodes_expanded = 0
    
    while stack:
        state, path = stack.pop()
        nodes_expanded += 1
        
        if state == goal:
            return path, nodes_expanded
        
        if len(path) > max_depth:
            continue
            
        for neighbor in get_surrounding_tiles(state):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))
    
    return None, nodes_expanded


def merge_paths(front_start, front_goal, meet):
    """
    Called by BDS
    Takes 3 arguments one being the front_start that is a dictionary of the parents starting from the starting state
    The front goal is the dictionary of parents starting from the goal state
    The meet is the state where the search from both states meet
    This function will return the two paths combined
    """
    path1 = reconstruct_path(front_start, meet)
    path2 = reconstruct_path(front_goal, meet)[::-1]
    return path1 + path2[1:]


def get_surrounding_tiles(state):
    """
    Takes in one argument state that it a tuple representing the current state of the board
    This function will generate all valid moves based on the location of the 0
    This function will return all possible valid board states after one move
    """
    neighbors = []
    # Calculates width and height, the sliding puzzle game will always be a square number
    size = int(len(state) ** 0.5)
    # Gets position of the blank tile, aka 0
    zero_index = state.index(0)
    # converts the tuple into a row column format
    row, col = divmod(zero_index, size)
    
    # Get valid moves, without moving off the board
    moves = []
    if row > 0: 
        moves.append((-1, 0))
    if row < size-1:
        moves.append((1, 0))
    if col > 0:
        moves.append((0, -1))
    if col < size-1:
        moves.append((0, 1))
    
    # Computes valid moves to see the new state
    # Makes new_state a list of the state so we can swap values around
    # Adds the move into neighbors array for returning all possible new states
    for dr, dc in moves:
        r, c = row + dr, col + dc
        new_index = r * size + c
        new_state = list(state)
        new_state[zero_index], new_state[new_index] = new_state[new_index], new_state[zero_index]
        neighbors.append(tuple(new_state))
    
    return neighbors


def reconstruct_path(parent, state):
    """
    Takes two arguments, parent being the dictionary of states and the value being the state that led to it
    The state argument is the goal state that the program reached
    """
    path = []
    # Will iterate until it has no more key value pairs of states
    while state is not None:
        path.append(state)
        state = parent[state]
    # Returns the list of steps in reverse order from start to goal
    return path[::-1]


def astar(start, goal, heuristic):
    """
    This function takes 3 arguments
    start is the current configuration of the puzzle
    goal is the desired configuration of the board
    heuristic is either manhattan or misplaced
    this will return the path and number of nodes expanded if they are found
    """
    # Creates a priority queue, will always return the lowest f score first
    open_set = []
    heapq.heappush(open_set, (0, 0, start))
    
    # Dictionaries to track costs and parents
    g_score = {start: 0}
    parent = {start: None}
    
    # Always keep a visited set to ensure you dont loop needlessly
    visited = set()
    nodes_expanded = 0
    
    while open_set:
        current_f_score, current_g_score, current_state = heapq.heappop(open_set)
        nodes_expanded += 1
        
        # Skip if we've found a better path to this node
        if current_state in visited:
            continue
            
        visited.add(current_state)
        
        if current_state == goal:
            return reconstruct_path(parent, current_state), nodes_expanded
        
        for neighbor in get_surrounding_tiles(current_state):
            if neighbor in visited:
                continue
                
            # Calculate tentative g_score
            tentative_g = g_score[current_state] + 1
            
            # If this path to neighbor is better than any previous one
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                parent[neighbor] = current_state
                g_score[neighbor] = tentative_g
                
                # Calculate f_score = g_score + heuristic
                if heuristic == 'manhattan':
                    h_score = manhattan_heuristic(neighbor, goal)
                else:
                    h_score = misplaced_tiles_heuristic(neighbor, goal)
                    
                # Add to the priority queue to explore later in the program if needed
                f_score = tentative_g + h_score
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))
    
    return None, nodes_expanded


def manhattan_heuristic(state, goal):
    """
    This function takes two arguments
    state which is the current configuration of the board
    goal which is the desired state of the board
    This function will return to total distance the tiles are from their goal position
    """
    size = int(len(state) ** 0.5)
    total_distance = 0
    
    for i, tile in enumerate(state):
        if tile == 0:
            continue
            
        # This gets the current position of the tile to check
        current_row, current_col = divmod(i, size)
        
        # This gets the goal position of that same tile 
        goal_index = goal.index(tile)
        goal_row, goal_col = divmod(goal_index, size)
        
        # This adds the distance of that tile to the total distance tracking variable
        total_distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    
    return total_distance


def misplaced_tiles_heuristic(state, goal):
    """
    This function takes two arguments
    state which is the current configuration of the puzzle
    goal which is the desired configuration of the goal
    This function will return the count of how many tiles are not in their desired position
    """
    misplaced = 0
    for i in range(len(state)):
        if state[i] != goal[i] and state[i] != 0:  # don't count blank tile
            misplaced += 1
    return misplaced


if __name__ == '__main__':
    main()