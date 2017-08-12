#include "BookRepository.h"

#include <iostream>

using namespace std;

void BookRepository::open() {
	_fp.open("book.dat", ios::out | ios::app);
}

void BookRepository::close() {
	_fp.close();
}

void BookRepository::addBook(const Book& book) {
	_fp.write((char*)&book, sizeof(Book));
}