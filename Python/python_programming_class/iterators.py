def iterator_decorator(func):
    def func_wrapper(string_tuple):
        print(f'Executing {func.__name__} with tuple: {string_tuple}')
        func(string_tuple)
    return func_wrapper

@iterator_decorator
def iter_function(string_tuple):
    first_tuple_iterator = iter(string_tuple)
    print(next(first_tuple_iterator))
    print(next(first_tuple_iterator))
    print(next(first_tuple_iterator))
    try:
        print(next(first_tuple_iterator))
    except StopIteration:
        print('StopIteration error raised')

@iterator_decorator
def iter_method(string_tuple):
    first_tuple_iterator = string_tuple.__iter__()
    print(first_tuple_iterator.__next__())
    print(first_tuple_iterator.__next__())
    print(first_tuple_iterator.__next__())
    try:
        print(first_tuple_iterator.__next__())
    except StopIteration:
        print('StopIteration error raised')


def main():
    first_tuple = ('apple', 'banana', 'cherry')
    iter_function(first_tuple)
    print()
    iter_method(first_tuple)


if __name__ == '__main__':
    main()