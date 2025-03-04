def return_fibonacci_number(**kwargs):
    num1             = kwargs.get('num1', 1)
    num2             = kwargs.get('num2', 1)
    iterations       = kwargs.get('iterations', 3)
    number_to_return = kwargs.get('number_to_return', 1)
    if iterations == number_to_return:
        print(f"The {number_to_return} num in the Fibonacci sequence is {num1 + num2}")
    else:
        return_fibonacci_number(num1=num2, num2=num1+num2, iterations=iterations + 1, number_to_return=number_to_return)


def main():
    num = 12
    if num <= 0:
        print(f"{num} is invalid input for the Fibonacci sequance")
    elif num <= 2:
        print(f"The {num} num in the Fibonacci sequence is 1")
    else:
        return_fibonacci_number(number_to_return=num)


if __name__ == "__main__":
    main()