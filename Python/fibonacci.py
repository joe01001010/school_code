def return_fibonacci_number(number, memo={}):
    if number in memo:
        return memo[number]

    if number <=0:
        return 0
    
    if number <= 2:
        return 1
    
    result = return_fibonacci_number(number-1, memo) + return_fibonacci_number(number-2, memo)
    memo[number] = result
    return result



def main():
    num = 999
    print(return_fibonacci_number(num))


if __name__ == "__main__":
    main()