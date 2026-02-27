#!/usr/bin/env python3

import datetime
import threading, time


def sleep_for_specified_time(seconds):
    start = datetime.datetime.now()
    time.sleep(seconds)
    print(f"Slept for {seconds} seconds")
    print("Was inside sleep for specified time function for", datetime.datetime.now() - start, "seconds")    


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


    thread_object_1 = threading.Thread(target = sleep_for_specified_time, args = [7])
    thread_object_2 = threading.Thread(target = sleep_for_specified_time, args = [10])
    thread_object_1.start()
    thread_object_2.start()


if __name__ == '__main__':
    main()
