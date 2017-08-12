#include "WordList_p.h"

#include <cstdlib>
#include <ctime>

using namespace std;

string randomDictionaryWord() {
	string words[] = {
		"india",
		"pakistan",
		"nepal",
		"malaysia",
		"philippines",
		"australia",
		"iran",
		"ethiopia",
		"oman",
		"indonesia"};

	srand(time(NULL));
	int n = rand() % 10;
	return words[n];	
}
