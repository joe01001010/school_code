import re

def match_string(string):
    pattern = r'[a-zA-Z0-9]*[A-Z][a-z]'
    match = re.match(pattern, string)
    if match:
        print(True)
    else:
        print(False)

def main():
    strings = ['abcdefg_hijklmnop', 'AwerA', 'aWER123','aAwer', 'asdAui!@#']
    for string in strings:
        match_string(string)

if __name__ == '__main__':
    main()