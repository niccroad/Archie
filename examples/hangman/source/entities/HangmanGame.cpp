#include "HangmanGame.h"

#include <iostream>

#include "WordList_p.h"

using namespace std;

const int MAX_TRIES = 5;

HangmanGame::HangmanGame() 
    : num_of_wrong_guesses(0)
{
	word = randomDictionaryWord();
	unknown = string(word.length(), '*');
}

void HangmanGame::playLoop() {
	// welcome the user
	cout << "\n\nWelcome to hangman...Guess a country Name";
	cout << "\n\nEach letter is represented by a star.";
	cout << "\n\nYou have to type only one letter in one try";
	cout << "\n\nYou have " << MAX_TRIES << " tries to try and guess the word.";
	cout << "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~";
    
	// Loop until the guesses are used up
	while (num_of_wrong_guesses < MAX_TRIES)
	{
		cout << "\n\n" << unknown;
		cout << "\n\nGuess a letter: ";
		char letter;
		cin >> letter;
		// Fill secret word with letter if the guess is correct,
		// otherwise increment the number of wrong guesses.
		if (letterFill(letter, word, unknown) == 0) {
			cout << endl << "Whoops! That letter isn't in there!" << endl;
			num_of_wrong_guesses++;
		} else {
			cout << endl << "You found a letter! Isn't that exciting!" << endl;
		}
		// Tell user how many guesses has left.
		cout << "You have " << MAX_TRIES - num_of_wrong_guesses;
		cout << " guesses left." << endl;
		// Check if user guessed the word.
		if (word == unknown) {
			cout << word << endl;
			cout << "Yeah! You got it!";
			break;
		}
	}
	if (num_of_wrong_guesses == MAX_TRIES) {
		cout << "\nSorry, you lose...you've been hanged." << endl;
		cout << "The word was : " << word << endl;
	}
	cin.ignore();
	cin.get();
}

int HangmanGame::letterFill(char guess, string secretword, string& guessword) {
	int i;
	int matches=0;
	int len=secretword.length();
	for (i = 0; i< len; i++)
	{
		// Did we already match this letter in a previous guess?
		if (guess == guessword[i])
			return 0;
		// Is the guess in the secret word?
		if (guess == secretword[i])
		{
			guessword[i] = guess;
			matches++;
		}
	}
	return matches;
}
