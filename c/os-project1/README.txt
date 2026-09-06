Members:
Joseph Weibel
We have neither given nor received unauthorized assistance on this work

Directory: jweibel
VM: weibelj-virtual-machine
Code Path: /opt/os-project1
Username: grader
Password: grader


General Description:
This project will create a linked list in C using structs referenced as a node datatype as well as a struct referenced as a list that will have a pointer to the head of the linked list. This project implements functions for adding nodes to the existing list pointer, removing nodes from the list pointer, printing the entire linked list, as well as flushing and freeing the linked list. The difference between flush and free are that the entire memory alloced to the list, including all items in the list will be freed. This means the list in its entirity will be cleared and unusable. Using flush_list will only remove all the elements from the list and enable the head pointer of the same linked list to be used to start a new list. This project also contains a file for testing all the different capabilities of the linked list implementation. This project includes a Makefile that can be used to compile the code for execution.


How to build and run the program:
1. cd /opt/os-project1
2. make
3. ./list_test


Description of the different pieces:
1. README.txt - This file will contain documentation on the project
2. Makefile - This file is used to create a reusable method to compile and clean up the project directory. Also defined dependencies for compiling.
3. list.c - This is the source code for the list creation, insertion, removal, printing, flushing, and freeing
4. list.h - Defined the structs and the function definitions
5. list_test.c - Contains a main function that will call separate functions that will test different functions from list.c


Challenges:
I have never made a Makefile before so I spent some time reading documentation on that. I was able to use the link provided in the assignment to format my makefile.
I have coded in C prior to this but I had to refresh myself on this and remember certain syntaxes and how pointers work.


Resources Used:
https://www.cs.colby.edu/maxwell/courses/tutorials/maketutor/
https://www.gnu.org/software/gnu-c-manual/gnu-c-manual.html
