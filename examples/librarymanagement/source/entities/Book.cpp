#include "Book.h"

#include <cstdio>
#include <iomanip>
#include <iostream>

using namespace std;

void Book::create_book() {
	cout << "\nNEW BOOK ENTRY...\n";
	cout << "\nEnter The book no.";
	cin >> bno;
	cout << "\n\nEnter The Name of The Book ";
	gets_s(bname, 50);
	cout << "\n\nEnter The Author's Name ";
	gets_s(aname, 20);
	cout << "\n\n\nBook Created..";
}

void Book::show_book() {
	cout<<"\nBook no. : "<<bno;
	cout<<"\nBook Name : ";
	puts(bname);
	cout<<"Author Name : ";
	puts(aname);
}

void Book::modify_book() {
	cout<<"\nBook no. : "<<bno;
	cout<<"\nModify Book Name : ";
	gets_s(bname, 50);
	cout<<"\nModify Author's Name of Book : ";
	gets_s(aname, 20);
}

char* Book::retbno() {
	return bno;
}

void Book::report() {
    cout << bno << setw(30) << bname << setw(30) << aname << endl;
}
