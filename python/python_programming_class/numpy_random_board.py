import numpy as np



def main():
    print("1 dimenstional array / vector:")
    python_list = [1,2,3,4,5]
    numpy_array = np.array(python_list)
    print("Python list:", python_list)
    print("Numpy array:", numpy_array)
    print("Numpy array converted back to list:", numpy_array.tolist())
    print()

    print("2 dimensional array / matrix")
    python_list_2 = [[1,2,3],[4,5,6],[7,8,9]]
    numpy_array_2 = np.array(python_list_2)
    print("Python 2 dimensional list:", python_list_2)
    print("Numpy matrix:", numpy_array_2)
    print("Numpy matrix converted back to python list:", numpy_array_2.tolist())
    print()


    board = np.random.randint(0,15, size=(3,3))
    print(board.dtype)
    print(board)
    print()

    fifteen = np.zeros(3, dtype='int64') + 15
    print(fifteen.dtype)
    print(fifteen)
    print()
    
    sum_of_columns = np.sum(board, axis=0)
    print(sum_of_columns)
    print(np.array_equal(sum_of_columns, fifteen))
    print()

    sum_of_rows = np.sum(board, axis=1)
    print(sum_of_rows)
    print(np.array_equal(sum_of_rows, fifteen))
    print()



if __name__ == '__main__':
    main()