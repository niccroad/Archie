#ifndef BookRepository_H
#define BookRepository_H

#include <fstream>

#include "IBookRepository.h"

class BookRepository : public IBookRepository {
public:
	void open() override;
	void close() override;
	void addBook(const Book& book) override;
	
private:
	std::fstream _fp;
};

#endif
