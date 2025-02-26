def test_decorator(function):
    def function_wrapper(number):
        print(f"Statement from inside decorator prior to {function.__name__} executing")
        function(number)
        print(f"Statement from inside decorator after {function.__name__} executing")
    return function_wrapper

@test_decorator
def square_number(number):
    print(f"The square of {number} is {number * number}")

def cube_number(number):
    print(f"The cube of {number} is {number * number * number}")

def lower_case_decorator(function):
    def function_wrapper(string):
        print(f"Inside decorator for lower case before function {function.__name__}")
        make_lowercase = function(string).lower()
        print(f"Inside decorator for lower case after function {function.__name__}")
        return make_lowercase
    return function_wrapper

def split_string_decorator(function):
    def function_wrapper(string):
        print(f"Inside decorator for split string before function {function.__name__}")
        split_string = function(string).split()
        print(f"Inside decorator for split string after function {function.__name__}")
        return split_string
    return function_wrapper

@split_string_decorator
@lower_case_decorator
def string_test_function(string):
    print(f"Input string is {string}")
    return string

class MultipleOfFive:
    def __init__(self, minimum, maximum):
        for value in range(minimum, maximum):
            if value % 5 == 0:
                break
        self.minimum = value
        self.maximum = maximum

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.minimum < self.maximum:
            result = self.minimum
            self.minimum += 5
            return result
        else:
            raise StopIteration
        
def multiples_of_five(minimum, maximum):
    for value in range(minimum, maximum):
        if value % 5 == 0:
            yield value



def main():
    # Permanent decorator
    square_number(10)

    print()
    print("Alternative approach to decorators")
    print()

    # Temporary decorator
    cube_number_decorator = test_decorator(cube_number)
    cube_number_decorator(10)

    print()
    print("Multiple decorators")
    print()

    # Multiple permanent decorators for one function
    print(f"Output from the double wrapper: {string_test_function('HELLO WORLD')}")
    print()

    # Iterators and Generators
    min = 12
    max = 123
    print("Generator and iterator class: ", end='')
    for value in MultipleOfFive(min, max):
        print(value, end = " ")
    print("",end="\n\n")

    # Build a generator that returns multiples of 5 between min and max
    print("Generators: ", end='')
    for value in multiples_of_five(min, max):
        print(value, end = " ")
    print("",end="\n\n")

    # Build a list comprehension that returns multiples of 5 between min and max
    values = [value for value in range(min, max) if value % 5 == 0]
    print(f"List comprehension: {values}")
    print()

    # Build a generator expression that returns multiples of 5 between min and max
    values = (value for value in range(min, max) if value % 5 == 0)
    print("Generator expression: ", end='')
    for value in values:
        print(value, end = " ")
    print()

if __name__ == "__main__":
    main()