#!/usr/bin/env python3

def debug_wrapper_function(func):
    def debug(graph, start):
        print(f"Executing {func.__name__}")
        func(graph, start)
    return debug


class Graph:
    graph = {
        'f': ['g', 'i'],
        'g': ['h'],
        'h': ['g'],
        'i': ['g', 'k'],
        'j': ['i'],
        'k': []
    }


@debug_wrapper_function
def depth_first_print_iterative(graph, start):
    stack = [start]
    while stack:
        current = stack.pop()
        print(current)

        for neighbor in graph[current]:
            stack.append(neighbor)


@debug_wrapper_function
def depth_first_print_recursive(graph, start):
    print(start)
    graph[start]
    for neighbor in graph[start]:
        depth_first_print_recursive(graph, neighbor)


@debug_wrapper_function
def breadth_first_print_iterative(graph, start):
    queue = [start]
    while queue:
        current = queue.pop(0)
        print(current)
        for neighbor in graph[current]:
            queue.append(neighbor)


def does_path_exist(graph, src, dest):
    if src not in graph:
        return False
    if src == dest:
        return True
    
    stack = [src]
    visited = set()
    while stack:
        current = stack.pop()
        if current == dest:
            return True
        if current in visited:
            continue
        visited.add(current)

        for neighbor in graph[current]:
            stack.append(neighbor)
    return False


def main(myGraph):
    print(does_path_exist(myGraph, 'j', 'f'))


if __name__ == '__main__':
    main(Graph.graph)