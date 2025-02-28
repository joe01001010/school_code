def factorial(number):
    # Or a one liner return 1 if number == 0 else number * factorial(number - 1)
    if number == 0:
        return 1
    else:
        factorial = 1
        for i in range(1, number  + 1):
            factorial *= i
        return factorial

def main():
    user_num = input("Enter a number to see the factorial: ")
    print(factorial(int(user_num)))

if __name__ == "__main__":
    main()