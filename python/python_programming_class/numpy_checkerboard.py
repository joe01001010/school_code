import numpy as np


def main():
    dimension = int(input("Please enter the dimension: "))
    board = np.zeros((dimension, dimension))
    board = board.astype(int)
    board[::2, ::2] = 1
    board[1::2, 1::2] = 1

    print(board)
    


if __name__ == '__main__':
    main()