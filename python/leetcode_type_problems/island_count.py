#!/usr/bin/env python3

def explore_island(grid, row, column, visited):
    row_inbounds = 0 <= row and row < len(grid)
    column_ibounds = 0 <= column and column < len(grid[1])
    if not row_inbounds or not column_ibounds:
        return False
    
    if grid[row][column] == 'W':
        return False

    position = str(row) + ',' + str(column)
    if position in visited:
        return False
    visited.add(position)

    explore_island(grid, row - 1, column, visited)
    explore_island(grid, row + 1, column, visited)
    explore_island(grid, row, column - 1, visited)
    explore_island(grid, row, column + 1, visited)

    return True


def island_count(grid):
    count = 0
    visited = set()
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if explore_island(grid, i, j, visited):
                count += 1
    return count


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

    print(f"Number of islands: {island_count(grid)}")


if __name__ == '__main__':
    main()