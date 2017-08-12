#include "Student.h"

#include <cstdio>
#include <iomanip>
#include <iostream>

using namespace std;

void Student::create_student() {
	system("clr");
	cout<<"\nNEW STUDENT ENTRY...\n";
	cout<<"\nEnter The admission no. ";
	cin>>admno;
	cout<<"\n\nEnter The Name of The Student ";
	gets_s(name, 20);
	token=0;
	stbno[0]='/0';
	cout<<"\n\nStudent Record Created..";
}

void Student::show_student() {
	cout<<"\nAdmission no. : "<<admno;
	cout<<"\nStudent Name : ";
	puts(name);
	cout<<"\nNo of Book issued : "<<token;
	if(token==1)
	cout<<"\nBook No "<<stbno;
}

void Student::modify_student() {
	cout<<"\nAdmission no. : "<<admno;
	cout<<"\nModify Student Name : ";
	gets_s(name, 32);
}

char* Student::retadmno() {
	return admno;
}

char* Student::retstbno() {
	return stbno;
}

int Student::rettoken() {
	return token;
}

void Student::addtoken() {
    token=1;
}

void Student::resettoken() {
    token=0;
}

void Student::getstbno(char t[]) {
	strcpy(stbno,t);
}

void Student::report() {
    cout << "\t" << admno << setw(20) << name << setw(10) << token << endl;
}