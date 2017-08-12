#ifndef Book_H
#define Book_H

class Book {
	char bno[6];
	char bname[50];
	char aname[20];
public:
	void create_book();
	void show_book();
	void modify_book();
	char* retbno();
	void report();
};

#endif
