def shortest_path(graph, nodeA, nodeB):
    # Initialize the visited nodes on a graph to a set for O(1) lookup times
    visited = set()
    # Use a queue since I am doing breadth first search
    queue = []
    # Initialize the queue with the node I am looking for
    queue.append([nodeA, 0])

    # This loop will search until the queue is empty and if it exhausts all options the function will return -1
    while queue:
        # Since we are adding to the queue using append() we need to pop from index 0
        current = queue.pop(0)
        # Check if current node is in visited and skip iteration if it is
        if current[0] in visited:
            continue
        # Add node to visited so we dont visit more than once
        visited.add(current[0])
        # Check if out current node is what we are looking for and if so return now with distance from starting node
        if current[0] == nodeB:
            return current[1]
        # append neighbors from graph to queue so we can search all nodes
        # Ensure to increment the counter for how far this node is from the starting node
        for neighbor in graph[current[0]]:
            queue.append([neighbor, current[1] + 1])
    return -1
        


def create_graph_undirected(edges):
    graph = {}
    for u, v in edges:
        if u not in graph:
            graph[u] = []
        graph[u].append(v)

        if v not in graph:
            graph[v] = []
        graph[v].append(u)
    return graph


def create_graph_directed(edges):
    graph = {}
    for u, v in edges:
        if u not in graph:
            graph[u] = []
        graph[u].append(v)
    return graph


def main():
    edges = [
        ['w', 'x'],
        ['x', 'y'],
        ['z', 'y'],
        ['z', 'v'],
        ['w', 'v']
    ]
    nodeA = 'w'
    nodeB = 'z'

    graph = create_graph_undirected(edges)
    shortest_path(graph, nodeA, nodeB)
    print(f"The shortes path between {nodeA} and {nodeB} is: {shortest_path(graph, nodeA, nodeB)}")



if __name__ == '__main__':
    main()