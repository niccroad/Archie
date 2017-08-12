#ifndef HangmanGame_H
#define HangmanGame_H

#include <string>

class HangmanGame {
public:
	HangmanGame();
	
	void playLoop();
	
private:
	int letterFill(char guess, std::string secretword, std::string& guessword);
	
private:
	int num_of_wrong_guesses;
	std::string word;
	std::string unknown;
};

#endif
