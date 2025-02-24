def reverse_string(string):
    for char in string[::-1]:
        yield char


def main():
    string = "Hello World"
    for char in reverse_string(string):
        print(char, end='')


if __name__ == "__main__":
    main()