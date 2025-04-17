import datetime
import threading, time


def calculate(a, b, c):
    start = datetime.datetime.now()
    result = a + b + c
    time.sleep(5)
    print(result)
    print("Time inside function:", datetime.datetime.now() - start)


def main():
    start = datetime.datetime.now()
    print("Start of program")
    thread_object = threading.Thread(target = calculate, args = [1, 2, 3])
    thread_object.start()
    print("End of program")
    print("Total time elapsed in main:", datetime.datetime.now() - start)


if __name__ == '__main__':
    main()