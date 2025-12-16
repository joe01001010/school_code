#include <iostream>
#include <cstdlib>
#include <ctime>
using namespace std;

class GuessTheNumber {
    // hidden representation of the number to guess HIDDEN
    private:
        int number_to_guess = rand() % 100 + 1;
    

    // Public methods EXPOSED
    public:
        GuessTheNumber() {
            srand(time(0));
            number_to_guess = rand() % 100 + 1;
        }
        // Exposed operation: check a guess
        bool checkGuess(int guess) const {
            return guess == number_to_guess;
        }
    
        // Exposed operation: give a hint
        string hint(int guess) const {
            if (guess < number_to_guess)
                return "Too low!";
            else if (guess > number_to_guess)
                return "Too high!";
            else
                return "Correct!";
        }
    };

int main() {
    GuessTheNumber game;
    int guess;
    cout << "Guess the number between 1 and 100: ";
    do {
        cout << "Enter your guess: ";
        cin >> guess;
        cout << game.hint(guess) << endl;
    } while (!game.checkGuess(guess));
    cout << "You guessed the number correctly!" << endl;
    return 0;
}