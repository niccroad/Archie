#ifndef Student_H
#define Student_H

class Student
{
	char admno[6];
	char name[20];
	char stbno[6];
	int token;
public:
	void create_student();
	void show_student();
	void modify_student();
    char* retadmno();
	char* retstbno();
	int rettoken();
	void addtoken();
	void resettoken();
	void getstbno(char t[]);
	void report();
};

#endif
