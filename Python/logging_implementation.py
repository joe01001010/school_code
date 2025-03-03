import logging
logging.basicConfig(filename='factorial_log_file.txt',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def factorial(**kwargs):
    number = kwargs.get('number', 0)
    logging.debug(f"Beginning to calculate factorial of {number}")
    total = 1
    for i in range(1, number + 1):
        total *= i
        logging.debug(f"Intermediate factorial value at step {i} is {total}")
    logging.debug(f"Completed calculation of factorial of {number}")
    return total

def main():
    #logging.disable()
    print(factorial(number=5))
    print(factorial(number=10))

if __name__ == "__main__":
    main()
    