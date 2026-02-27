#!/usr/bin/env python3

def factorial(number):
    factorial = 1
    if number == 0 or number == 1:
        return factorial
        
    for i in range(1, number + 1):
        factorial *= i
    return factorial

def main():
    num1 = 900
    print(f"Factorial of {num1} is {factorial(num1)}")
    print(f"The length of the factorial of {num1} is {len(str(factorial(num1)))} characters")

if __name__ == "__main__":
    main()