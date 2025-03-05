def pascals_triangle(rows):
    triangle = []
    for i in range(rows):
        row = [1]
        if triangle:
            last_row = triangle[-1]
            row.extend([sum(pair) for pair in zip(last_row, last_row[1:])])
            row.append(1)
        triangle.append(row)
    return triangle
    

def main():
    print(pascals_triangle(300))

if __name__ == "__main__":
    main()