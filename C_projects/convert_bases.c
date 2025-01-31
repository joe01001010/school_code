/*
  =========================================================================
  PROGRAMMER:..... Joseph Weibel
  FILE NAME:...... pj02b.c
  ASSIGNMENT:..... PJ02B
  PROBLEM:........ B
  DUE DATE:....... 17 NOV 2024
  COURSE:......... CS-2160
  SECTION:........ 001
  SEMESTER:....... Fall 2024
  =========================================================================
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

#define FILE_NAME_SIZE 100
#define FILE_LINE_SIZE 100
#define NUMBER_SIZE 50
#define BASE_SIZE 3
#define VALUE_SIZE 2

void removeNewline(char* str);
short charToValue(const char character);
void parseLine(const char* line, char* number, char* baseFrom, char* baseTo);
long convertToBaseTen(const char* number, const char* baseFrom);
char converToNewBase(const long number, const char* baseTo, char* finalString);
void valueToChar(const int remainder, char* destValue);
void reverseString(char* string);
void shiftNumberLeft(char* string);

int main(int argc, char* argv[]) {
	char filename[FILE_NAME_SIZE] = { '\0' };
	long runningIntegerTotal = 0;

	// If this is not called from the cmd line it will ask for the file name
	if (argc != 2) {
		fgets(filename, FILE_NAME_SIZE, stdin);
		removeNewline(filename);
	}
	else {
		for (size_t index = 0; index < strlen(argv[1]); index++){
			filename[index] = argv[1][index];
		}
	}
	
	// Read the file line by line and print the headers before the loop
	FILE* numberFile = fopen(filename, "r");
	char currentLine[FILE_LINE_SIZE] = { '\0' };
	puts("\t\t    INPUT FM TO\t\t\t   RESULT    DECIMAL");
	puts("------------------------- -- -- ------------------------- ----------");
	while (fgets(currentLine, sizeof(currentLine), numberFile) != NULL) {
		char finalStringValue[NUMBER_SIZE] = { '\0' };
		char startingNumber[NUMBER_SIZE] = { '\0' };
		char baseFrom[BASE_SIZE] = { '\0' };
		char baseTo[BASE_SIZE] = { '\0' };
		char* endptr;
		long longStartingNumber = 0;
		// Break the line into the number, base from, and base to
		// This will read until the first comma and set the number
		// Then it will read until the second comma and set the base from
		// Finally it will read until the end of the line and set the base to
		parseLine(currentLine, startingNumber, baseFrom, baseTo);

		// Check if base from is 10 and if it is we will skip converting to base 10
		int comparisonResult = strcmp(baseFrom, "10");
		if (comparisonResult != 0) {
			// This function returns a long and expectes two char* as arguments
			// The first argument is the number to convert and the second is the base to convert from
			longStartingNumber = convertToBaseTen(startingNumber, baseFrom);
			//Increment the total of all the numbers
			runningIntegerTotal += longStartingNumber;
		}
		else {
			// This function will convert the string to a long and return the value
			// This will only execute if the base from is 10
			longStartingNumber = strtol(startingNumber, &endptr, 10);
			//Increment the total of all the numbers
			runningIntegerTotal += longStartingNumber;
		}
		
		// Check if the base to convert to is 10 and if it is we will skip conversion
		comparisonResult = strcmp(baseTo, "10");
		if (comparisonResult != 0) {
			// This function will convert the number to the new base
			// This function expects a long, a char*, and a char* as arguments
			// This function doesnt return anything it will modify the finalStringValue memory address
			converToNewBase(longStartingNumber, baseTo, finalStringValue);
		}
		else {
			itoa(longStartingNumber, finalStringValue, 10);
		}
		while (finalStringValue[0] == '0' && strlen(finalStringValue) > 1) {
			//This will iterate in order to remove all the leading zeros from the number
			shiftNumberLeft(finalStringValue);
		}

		printf("%25s %2s %2s %25s %10ld\n",startingNumber, baseFrom, baseTo, finalStringValue, longStartingNumber);

	}
	//Print final format line with all the total
	puts("------------------------- -- -- ------------------------- ----------");
	printf("\t\t\t\t\t\t    Total %10ld\n", runningIntegerTotal);

	//Close the file
	fclose(numberFile);
	return 0;
}


void removeNewline(char* str) {
	if (str[strlen(str)-1] == '\n') {
		str[strlen(str)-1] = '\0';
	}
}


short charToValue(const char character) {
	char tempCharacter = character;
	int value = 0;
	if (tempCharacter >= 'A' && tempCharacter <= 'Z') {
		value =  tempCharacter - 'A' + 10;
	}
	else if (tempCharacter >= 'a' && tempCharacter <= 'z') {
		value = tempCharacter - 'a' + 36;
	}
	else if (tempCharacter == '#') {
		value = 62;
	}
	else {
		value = 63;
	}
	
	return value;
}


void parseLine(const char* line, char* number, char* baseFrom, char* baseTo) {
	size_t baseFromIndex = 0;
	size_t baseToIndex = 0;

	for (size_t i = 0; i < strlen(line) - 1; i++) {
		if (line[i] == ',') {
			for (size_t j = i + 1; j < strlen(line) - 1; j++) {
				if (line[j] == ',') {
					for (size_t k = j + 1; k < strlen(line) - 1; k++) {
						baseTo[baseToIndex] = line[k];
						baseToIndex++;
					}
					j = strlen(line);
				}
				baseFrom[baseFromIndex] = line[j];
				baseFromIndex++;
			}
			i = strlen(line);
		}
		number[i] = line[i];
	}
}


long convertToBaseTen(const char* number, const char* baseFrom) {
	int base = atoi(baseFrom);
	long longNumber = 0;
	int tempPower = strlen(number) - 1;

	for (size_t i = 0; i < strlen(number); i++) {
		if (isdigit(number[i])) {
			int value = number[i];
			value = value - '0';
			longNumber += (long) value * pow(base, tempPower - i);
		}
		else {
			longNumber += (long) charToValue(number[i]) * pow(base, tempPower - i);
		}
	}

	return longNumber;
}


char converToNewBase(const long number, const char* baseTo, char* finalString) {
	int base = atoi(baseTo);
	long longNumber = 0;
	long startingNumber = number;
	long quotient = 0;
	int remainder = 0;
	int index = 0;
	char fullNumberString[NUMBER_SIZE] = { '\0' };


	do {
		char stringValue[VALUE_SIZE] = { '\0' };
		quotient = startingNumber / base;
		remainder = startingNumber % base;
		startingNumber = quotient;

		if (remainder < 10) {
			itoa(remainder, stringValue, 10);
		}
		else {
			valueToChar(remainder, stringValue);
		}
		fullNumberString[index] = stringValue[0];
		index++;

		if (base > startingNumber) {
			if (startingNumber < 10) {
				itoa(startingNumber, stringValue, 10);
			}
			else {
				valueToChar(startingNumber, stringValue);
			}
			fullNumberString[index] = stringValue[0];
		}
	} while (base < startingNumber);
	reverseString(fullNumberString);

	for (size_t i = 0; i < strlen(fullNumberString); i++) {
		finalString[i] = fullNumberString[i];
	}
}


void valueToChar(const int remainder, char* destValue) {
	char tempChar = '\0';
	if (remainder >= 10 && remainder <= 35) {
		tempChar = 'A' + (remainder - 10);
	}
	else if (remainder >= 36 && remainder <= 61) {
		tempChar = 'a' + (remainder - 36);
	}
	else if (remainder == 62) {
		tempChar = '#';
	}
	else {
		tempChar = '$';
	}
	destValue[0] = tempChar;

}


void reverseString(char* string) {
	char tempString[NUMBER_SIZE] = { '\0' };
	size_t length = strlen(string);

	for (size_t i = 0; i < strlen(string); i++) {
		tempString[i] = string[i];
	}
	for (size_t i = 0; i < strlen(string); i++) {
		string[i] = tempString[length - 1 - i];
	}

}


void shiftNumberLeft(char* string) {
	for (size_t i = 0; i < strlen(string); i++) {
		string[i] = string[i + 1];
	}
}