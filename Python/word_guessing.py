import requests
import bs4
import pandas as pd
import random


# This is the main function of the program
# The function will fetch data from a website
# The function will parse the data and save it to an excel file
# The function will get a random word from the excel file
# The function will call the word_guessing_game function with the random word
def main():
    url = 'https://www.ef.edu/english-resources/english-vocabulary/top-1000-words/'
    output_file = 'top_1000_words.xlsx'

    get_response = get_request_to_website(url=url)
    parsed_response = parse_response(response=get_response)
    save_to_excel(data=parsed_response, file=output_file)
    random_word = get_random_word(file=output_file)
    word_guessing_game(random_word)


# This function will take an argument of the random word to guess
# The function will then take user input to guess the word
# The function will display underscores for each letter in the word
# If the user guesses a letter correctly the underscore will be replaced with the letter
# If the user guesses a letter incorrectly the function will keep track of the number of mistakes
def word_guessing_game(word):
    word_length = len(word)
    word_list = list(word)
    guessed_word = ['_'] * word_length
    mistakes = 0
    print(" ".join(guessed_word))
    while mistakes < 5:
        letter = input("Enter a letter: ")
        if letter in word_list:
            for i in range(word_length):
                if word_list[i] == letter:
                    guessed_word[i] = letter
            print(" ".join(guessed_word))
            if '_' not in guessed_word:
                print(word)
                print("You won!")
                break
        else:
            mistakes += 1

    if mistakes >= 4:
        print("You lost!")
        print(word)
            

# This function will take an argument of the file name with the 'file' keyword
# The function will read the excel file and return a random word from the list
def get_random_word(**kwargs):
    file = kwargs.get('file')
    df = pd.read_excel(file)
    random_word = random.choice(df["Words"].tolist())
    return random_word


# This function will take an argument of the data to save and the file name with the 'data' and 'file' keywords
# The function will save the data to an excel file
def save_to_excel(**kwargs):
    data = kwargs.get('data')
    file = kwargs.get('file')
    df = pd.DataFrame(data, columns=['Words'])
    df.to_excel(file, index=False)


# This function will take an argument of the url to fetch data from
# The function will make a get request to the url
# The function will return the response unfiltered
def get_request_to_website(**kwargs):
    url = kwargs.get('url')
    response = requests.get(url=url)
    if response.status_code != 200:
        print(f"Failed to fetch data from {url}")
    return response


# This function will take an argument of the response to parse
# The function will parse the response and return a list of words
def parse_response(**kwargs):
    response = kwargs.get('response')
    soup = bs4.BeautifulSoup(response.content, 'html.parser')
    words = soup.find_all(name='div', class_='field-items')
    word_list = words[0].text.strip().replace('\t','').split('\n')
    sliced_word_list = word_list[2:]
    return sliced_word_list


# This is the entry point of the program
# The main function will be called when the script is run
if __name__ == '__main__':
    main()