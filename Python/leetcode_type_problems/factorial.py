import math

def factorial(number):
    # This function is useful to determine the number of possible combinations of a set of elements
    # Such as all the combinations of {a, b, c} are {a, b, c}, {a, c, b}, {b, a, c}, {b, c, a}, {c, a, b}, {c, b, a}
    # The factorial of 3 is 3! = 3 * 2 * 1 = 6
    # Or a one liner return 1 if number == 0 else number * factorial(number - 1)
    if number == 0 or number == 1:
        return 1
    elif number > 20:
        # This will use stirlings approximation to calculate the factorial of a large number
        # It is useful to calculate the factorial of a large number
        # The approximation is n! = sqrt(2 * pi * n) * (n / e)^n
        return int(math.sqrt(2 * math.pi * number) * ((number / math.e) ** number))
    else:
        factorial = 1
        for i in range(1, number + 1):
            factorial *= i
        return factorial

def main():
    num1 = 5
    print(f"Factorial of {num1} is {factorial(num1)}")
    print(f"The length of the factorial of {num1} is {len(str(factorial(num1)))} characters")

if __name__ == "__main__":
    main()