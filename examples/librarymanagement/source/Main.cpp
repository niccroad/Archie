#include <fstream>
#include <conio.h>
#include <cstdio>
#include <string>
#include <iomanip>
#include <iostream>

#include <windows.h>

void gotoxy(int column, int line) {
    COORD coord;
    coord.X = column;
    coord.Y = line;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), coord);
}

#include "Book.h"
#include "BookRepository.h"
#include "Student.h"
#include "LibraryActions.h"

using namespace std;

fstream fp,fp1;
Book bk;
Student st;

BookRepository bookRepo;

//***************************************************************
//    	function to write in file
//****************************************************************

void write_student()
{
	char ch;
	fp.open("student.dat",ios::out|ios::app);
	do
	{
		st.create_student();
		fp.write((char*)&st,sizeof(Student));
		cout<<"\n\ndo you want to add more record..(y/n?)";
		cin>>ch;
	}while(ch=='y'||ch=='Y');
	fp.close();
}


//***************************************************************
//    	function to read specific record from file
//****************************************************************


void display_spb(char n[])
{
	cout<<"\nBOOK DETAILS\n";
	int flag=0;
	fp.open("book.dat",ios::in);
	while(fp.read((char*)&bk,sizeof(Book)))
	{
		if(strcmpi(bk.retbno(),n)==0)
		{
			bk.show_book();
		 	flag=1;
		}
	}
	
	fp.close();
	if(flag==0)
		cout<<"\n\nBook does not exist";
	getch();
}

void display_sps(char n[])
{
	cout<<"\nSTUDENT DETAILS\n";
	int flag=0;
	fp.open("student.dat",ios::in);
	while(fp.read((char*)&st,sizeof(Student)))
	{
		if((strcmpi(st.retadmno(),n)==0))
		{
			st.show_student();
			flag=1;
		}
	}
	
	fp.close();
	if(flag==0)
    		cout<<"\n\nStudent does not exist";
 	getch();
}


//***************************************************************
//    	function to modify record of file
//****************************************************************


void modify_book()
{
	char n[6];
	int found=0;
	system("cls");
	cout<<"\n\n\tMODIFY BOOK REOCORD.... ";
	cout<<"\n\n\tEnter The book no. of The book";
	cin>>n;
	fp.open("book.dat",ios::in|ios::out);
	while(fp.read((char*)&bk,sizeof(Book)) && found==0)
	{
		if(strcmpi(bk.retbno(),n)==0)
		{
			bk.show_book();
			cout<<"\nEnter The New Details of book"<<endl;
			bk.modify_book();
			int pos=-1*sizeof(bk);
		    	fp.seekp(pos,ios::cur);
		    	fp.write((char*)&bk,sizeof(Book));
		    	cout<<"\n\n\t Record Updated";
		    	found=1;
		}
	}

    	fp.close();
    	if(found==0)
    		cout<<"\n\n Record Not Found ";
    	getch();
}


void modify_student()
{
	char n[6];
	int found=0;
	system("cls");
	cout<<"\n\n\tMODIFY STUDENT RECORD... ";
	cout<<"\n\n\tEnter The admission no. of The student";
	cin>>n;
	fp.open("student.dat",ios::in|ios::out);
	while(fp.read((char*)&st,sizeof(Student)) && found==0)
	{
		if(strcmpi(st.retadmno(),n)==0)
		{
			st.show_student();
			cout<<"\nEnter The New Details of student"<<endl;
			st.modify_student();
			int pos=-1*sizeof(st);
			fp.seekp(pos,ios::cur);
			fp.write((char*)&st,sizeof(Student));
			cout<<"\n\n\t Record Updated";
			found=1;
		}
	}
	
	fp.close();
	if(found==0)
		cout<<"\n\n Record Not Found ";
	getch();
}

//***************************************************************
//    	function to delete record of file
//****************************************************************


void delete_student()
{
	char n[6];
	int flag=0;	
	system("cls");
    	cout<<"\n\n\n\tDELETE STUDENT...";
    	cout<<"\n\nEnter The admission no. of the Student You Want To Delete : ";
    	cin>>n;
    	fp.open("student.dat",ios::in|ios::out);
    	fstream fp2;
    	fp2.open("Temp.dat",ios::out);
    	fp.seekg(0,ios::beg);
    	while(fp.read((char*)&st,sizeof(Student)))
	{
		if(strcmpi(st.retadmno(),n)!=0)
	     		fp2.write((char*)&st,sizeof(Student));
		else
	   		flag=1;
	}
    	
	fp2.close();
    	fp.close();
    	remove("student.dat");
    	rename("Temp.dat","student.dat");
    	if(flag==1)
     		cout<<"\n\n\tRecord Deleted ..";
    	else
     		cout<<"\n\nRecord not found";
    	getch();
}


void delete_book()
{
	char n[6];
	system("cls");
	cout<<"\n\n\n\tDELETE BOOK ...";
	cout<<"\n\nEnter The Book no. of the Book You Want To Delete : ";
	cin>>n;
	fp.open("book.dat",ios::in|ios::out);
	fstream fp2;
	fp2.open("Temp.dat",ios::out);
	fp.seekg(0,ios::beg);
	while(fp.read((char*)&bk,sizeof(Book)))
	{
		if(strcmpi(bk.retbno(),n)!=0)  
		{
			fp2.write((char*)&bk,sizeof(Book));
		}
	}
    	
	fp2.close();
    	fp.close();
    	remove("book.dat");
    	rename("Temp.dat","book.dat");
    	cout<<"\n\n\tRecord Deleted ..";
    	getch();
}



//***************************************************************
//    	function to display all students list
//****************************************************************

void display_alls()
{
	system("cls");
     	fp.open("student.dat",ios::in);
     	if(!fp)
     	{
       		cout<<"ERROR!!! FILE COULD NOT BE OPEN ";
       		getch();
       		return;
     	}

	cout<<"\n\n\t\tSTUDENT LIST\n\n";
	cout<<"==================================================================\n";
	cout<<"\tAdmission No."<<setw(10)<<"Name"<<setw(20)<<"Book Issued\n";
	cout<<"==================================================================\n";

	while(fp.read((char*)&st,sizeof(Student)))
	{
		st.report();
	}
     	
	fp.close();
	getch();
}


//***************************************************************
//    	function to display Books list
//****************************************************************

void display_allb()
{
	system("cls");
	fp.open("book.dat",ios::in);
	if(!fp)
	{
		cout<<"ERROR!!! FILE COULD NOT BE OPEN ";
       		getch();
       		return;
     	}

	cout<<"\n\n\t\tBook LIST\n\n";
	cout<<"=========================================================================\n";
	cout<<"Book Number"<<setw(20)<<"Book Name"<<setw(25)<<"Author\n";
	cout<<"=========================================================================\n";

	while(fp.read((char*)&bk,sizeof(Book)))
	{
		bk.report();
	}
     	fp.close();
     	getch();
}



//***************************************************************
//    	function to issue book
//****************************************************************

void book_issue()
{
	char sn[6],bn[6];
	int found=0,flag=0;
	system("cls");
	cout<<"\n\nBOOK ISSUE ...";
	cout<<"\n\n\tEnter The student's admission no.";
	cin>>sn;
	fp.open("student.dat",ios::in|ios::out);
    	fp1.open("book.dat",ios::in|ios::out);
    	while(fp.read((char*)&st,sizeof(Student)) && found==0)
       	{
		if(strcmpi(st.retadmno(),sn)==0)
		{
			found=1;
			if(st.rettoken()==0)
			{
		      		cout<<"\n\n\tEnter the book no. ";
				cin>>bn;
				while(fp1.read((char*)&bk,sizeof(Book))&& flag==0)
				{
			   		if(strcmpi(bk.retbno(),bn)==0)
					{
						bk.show_book();
						flag=1;
						st.addtoken();
						st.getstbno(bk.retbno());
       						int pos=-1*sizeof(st);
						fp.seekp(pos,ios::cur);
						fp.write((char*)&st,sizeof(Student));
						cout<<"\n\n\t Book issued successfully\n\nPlease Note: Write current date "
						"in backside of book and submit within 15 days fine Rs. 1 for each day " 	
						"after 15 days period";
					}
		    		}
		  		if(flag==0)
		    			cout<<"Book no does not exist";
			}
	    		else
		  		cout<<"You have not returned the last book ";

		}
	}
      	if(found==0)
		cout<<"Student record not exist...";
	getch();
  	fp.close();
  	fp1.close();
}

void book_deposit()
{
    char sn[6],bn[6];
    int found=0,flag=0,day,fine;
    system("cls");
    cout<<"\n\nBOOK DEPOSIT ...";
    cout<<"\n\n\tEnter The student’s admission no.";
    cin>>sn;
    fp.open("student.dat",ios::in|ios::out);
    fp1.open("book.dat",ios::in|ios::out);
    while(fp.read((char*)&st,sizeof(Student)) && found==0)
       {
	    if(strcmpi(st.retadmno(),sn)==0)
	    {
		    found=1;
		    if(st.rettoken()==1)
		    {
			while(fp1.read((char*)&bk,sizeof(Book))&& flag==0)
			{
			   if(strcmpi(bk.retbno(),st.retstbno())==0)
			{
				bk.show_book();
				flag=1;
				cout<<"\n\nBook deposited in no. of days";
				cin>>day;
				if(day>15)
				{
				   fine=(day-15)*1;
				   cout<<"\n\nFine has to deposited Rs. "<<fine;
				}
					st.resettoken();
					int pos=-1*sizeof(st);
					fp.seekp(pos,ios::cur);
					fp.write((char*)&st,sizeof(Student));
					cout<<"\n\n\t Book deposited successfully";
			}
		    }
		  if(flag==0)
		    cout<<"Book no does not exist";
		      }
		 else
			cout<<"No book is issued..please check!!";
		}
	   }
      if(found==0)
	cout<<"Student record not exist...";
	getch();
  fp.close();
  fp1.close();
  }




//***************************************************************
//    	INTRODUCTION FUNCTION
//****************************************************************

void intro()
{
	system("cls");
	gotoxy(35,11);
	cout<<"LIBRARY";
	gotoxy(35,14);
	cout<<"MANAGEMENT";
	gotoxy(35,17);
	cout<<"SYSTEM";
	cout<<"\n\nMADE BY : YOUR NAME";
	cout<<"\n\nSCHOOL : SCHOOL NAME";
	getch();
}



//***************************************************************
//    	ADMINISTRATOR MENU FUNCTION
//****************************************************************

void admin_menu()
{
	system("cls");
	int ch2;
	cout<<"\n\n\n\tADMINISTRATOR MENU";
	cout<<"\n\n\t1.CREATE STUDENT RECORD";
	cout<<"\n\n\t2.DISPLAY ALL STUDENTS RECORD";
	cout<<"\n\n\t3.DISPLAY SPECIFIC STUDENT RECORD ";
	cout<<"\n\n\t4.MODIFY STUDENT RECORD";
	cout<<"\n\n\t5.DELETE STUDENT RECORD";
	cout<<"\n\n\t6.CREATE BOOK ";
	cout<<"\n\n\t7.DISPLAY ALL BOOKS ";
	cout<<"\n\n\t8.DISPLAY SPECIFIC BOOK ";
	cout<<"\n\n\t9.MODIFY BOOK ";
	cout<<"\n\n\t10.DELETE BOOK ";
	cout<<"\n\n\t11.BACK TO MAIN MENU";
	cout<<"\n\n\tPlease Enter Your Choice (1-11) ";
	cin>>ch2;
	switch(ch2)
	{
    		case 1: system("cls");
	    		write_student();break;
    		case 2: display_alls();break;
    		case 3:
	       		char num[6];
	       		system("cls");
	       		cout<<"\n\n\tPlease Enter The Admission No. ";
	       		cin>>num;
	       		display_sps(num);
	       		break;
      		case 4: modify_student();break;
      		case 5: delete_student();break;
		case 6:
			system("cls");
			write_book(bookRepo);
			break;
		case 7: display_allb();break;
		case 8: {
	       		char num[6];
	       		system("cls");
	       		cout<<"\n\n\tPlease Enter The book No. ";
	       		cin>>num;
	       		display_spb(num);
	       		break;
			}
      		case 9: modify_book();break;
      		case 10: delete_book();break;
     		case 11: return;
      		default:cout<<"\a";
   	}
   	admin_menu();
}

void main() {
	char ch;
	intro();
	do {
		system("cls");
		cout << "\n\n\n\tMAIN MENU";
		cout << "\n\n\t01. BOOK ISSUE";
		cout << "\n\n\t02. BOOK DEPOSIT";
	  	cout << "\n\n\t03. ADMINISTRATOR MENU";
	  	cout << "\n\n\t04. EXIT";
	  	cout << "\n\n\tPlease Select Your Option (1-4) ";
	  	ch = getche();
	  	switch(ch) {
		case '1':
			system("cls");
			book_issue();
			break;
		case '2':
			book_deposit();
			break;
		case '3':
			admin_menu();
			break;
		case '4':
			exit(0);
		default:
			cout << "\a";
		}
    } while(ch != '4');
}