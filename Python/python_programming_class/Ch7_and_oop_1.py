import re

def match_string(string):
    pattern = r'^[a-z]+_[a-z]+$'
    match = re.match(pattern, string)
    if match:
        print(True)
    else:
        print(False)

def main():
    strings = ['abcdefg_hijklmnop', 'zyxwvuts_rqponmlk', 'abFdf_wer','asd4fg_werty']
    for string in strings:
        match_string(string)

if __name__ == '__main__':
    main()