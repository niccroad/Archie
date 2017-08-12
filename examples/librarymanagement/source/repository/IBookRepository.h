#ifndef IBookRepository_H
#define IBookRepository_H

#include "Book.h"

class IBookRepository {
public:
	virtual ~IBookRepository() { }
	
	virtual void open() = 0;
	virtual void close() = 0;

	virtual void addBook(const Book& book) = 0;
};

#endif
