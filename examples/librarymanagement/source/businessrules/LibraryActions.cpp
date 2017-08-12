#include "LibraryActions.h"

#include <iostream>

#include "Book.h"

using namespace std;

void write_book(IBookRepository& repository) {
	Book book;
	char ch;
	repository.open();
	do {
		system("cls");
		book.create_book();
		repository.addBook(book);
		cout << "\n\nDo you want to add more record..(y/n?)";
		cin >> ch;
	} while(ch=='y'||ch=='Y');
	repository.close();	
}