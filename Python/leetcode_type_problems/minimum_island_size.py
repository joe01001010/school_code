def smallest_island(grid):
    visited = set()
    smallest = 99999
    for r in range(0, len(grid)):
        for c in range(0, len(grid[0])):
            size = get_size(grid, r, c, visited)
            if size != 0 and size < smallest:
                smallest = size
    return smallest


def get_size(grid, row, column, visited):
    row_inbounds = 0 <= row and row < len(grid)
    column_inbounds = 0 <= column and column < len(grid[0])
    if not row_inbounds or not column_inbounds:
        return 0
    
    if grid[row][column] == 'W':
        return 0

    current = str(row) + ',' + str(column)
    if current in visited:
        return 0
    
    visited.add(current)

    island_size = 1
    island_size += get_size(grid, row, column - 1, visited)
    island_size += get_size(grid, row, column + 1, visited)
    island_size += get_size(grid, row - 1, column, visited)
    island_size += get_size(grid, row + 1, column, visited)

    return island_size

    
    


def main():
    grid = [
        ['W', 'L', 'W', 'W', 'W'],
        ['W', 'L', 'W', 'W', 'W'],
        ['W', 'W', 'W', 'L', 'W'],
        ['W', 'W', 'L', 'L', 'W'],
        ['L', 'W', 'W', 'L', 'L'],
        ['L', 'L', 'W', 'W', 'W']
    ]
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            print(grid[i][j], end=' ')
        print()
    print()

    print(f"Smallest island: {smallest_island(grid)}")


if __name__ == '__main__':
    main()