/*
  =========================================================================
  PROGRAMMER:..... Joseph Weibel
  FILE NAME:...... pj02c.c
  ASSIGNMENT:..... PJ02C
  PROBLEM:........ C
  DUE DATE:....... 17 NOV 2024
  COURSE:......... CS-2160
  SECTION:........ 001
  SEMESTER:....... Fall 2024
  =========================================================================
*/

#include <stdio.h>
#include <stdint.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <ctype.h>
#include <stdbool.h>
#include <inttypes.h>

#define MAX_NUMBER_LENGTH 100


void convertToNewBase(const long number, char* finalString);
void reverseString(char* string);
int returnByteCounter(const char* convertedString);
void addZerosToFront(char* string);
uint64_t convertToBaseTen(const char* number);
void clearString(char* string);
void removeLeadingZeros(char* string);
void removeUselessBits(char* string);
void shiftLeftTwo(char* string, const size_t currentIndex);
void createUtfEightString(char* combinedString, const size_t numBytes, FILE *fileOutput);
void checkLeadingOnes(const char* convertedByteString, size_t* noLeadingOnesCount, size_t* oneLeadingOneCount, size_t* twoLeadingOnesCount, size_t* threeLeadingOnesCount, size_t* fourLeadingOnesCount, size_t* fiveLeadingOnesCount, size_t* sixLeadingOnesCount, size_t* sevenLeadingOnesCount);

int main() {
	FILE* htmlFilePtr = fopen("UTF-8-demo.html", "rb");
	FILE* integersFilePtr = fopen("integers.bin", "rb");
	FILE* integersOutputFilePtr = fopen("integers.utf8", "wb");

	size_t totalByteCounter = 0;
	size_t numberOfValues = 0;
	size_t asciiCodes = 0;
	size_t noLeadingOnesCount = 0;
	size_t oneLeadingOneCount = 0;
	size_t twoLeadingOnesCount = 0;
	size_t threeLeadingOnesCount = 0;
	size_t fourLeadingOnesCount = 0;
	size_t fiveLeadingOnesCount = 0;
	size_t sixLeadingOnesCount = 0;
	size_t sevenLeadingOnesCount = 0;
	uint8_t byte = 0;
	uint64_t singleNum = 0;
	uint64_t runningTotal = 0;
	size_t fileReadResult = 0;
	char numberString[MAX_NUMBER_LENGTH] = { '\0' };
	char convertedByteString[MAX_NUMBER_LENGTH] = { '\0' };
	char allBytesCombinedString[MAX_NUMBER_LENGTH] = { '\0' };
	int byteCounter = 0;
	bool newNumber = true;
	bool multiByteNumber = false;
	uint32_t completeFourByteValue = 0;


	while (fileReadResult = fread(&byte, 1, 1, htmlFilePtr) == 1) {
		snprintf(numberString, sizeof(numberString), "%u", byte);
		convertToNewBase(byte, convertedByteString);
		checkLeadingOnes(convertedByteString, &noLeadingOnesCount, &oneLeadingOneCount, &twoLeadingOnesCount, &threeLeadingOnesCount, &fourLeadingOnesCount, &fiveLeadingOnesCount, &sixLeadingOnesCount, &sevenLeadingOnesCount);

		if (newNumber) {
			byteCounter = returnByteCounter(convertedByteString);
			if (byteCounter == 1) {
				asciiCodes++;
			}
			newNumber = false;
			clearString(allBytesCombinedString);
		}

		if (byteCounter > 0) {
			if (byteCounter > 1) {
				multiByteNumber = true;
			}

			size_t allBytesCombinedStringIndex = strlen(allBytesCombinedString);
			for (size_t i = 0; i < strlen(convertedByteString); i++) {
				allBytesCombinedString[allBytesCombinedStringIndex] = convertedByteString[i];
				allBytesCombinedStringIndex++;
			}

			byteCounter--;
		}
		
		if (byteCounter == 0) {
			removeUselessBits(allBytesCombinedString);
			singleNum = convertToBaseTen(allBytesCombinedString);
			runningTotal += singleNum;
			newNumber = true;
			multiByteNumber = false;
			numberOfValues++;
		}
		totalByteCounter++;
	}
	fclose(htmlFilePtr);


	printf("File size:...........%15zu bytes\n", totalByteCounter);
	printf("ASCII codes:.........%15zu codes\n", asciiCodes);
	printf("Number of values:....%15zu\n", numberOfValues);
	printf("Sum of values:.......%15zu\n", runningTotal);
	printf("Leading 1s: 0........%15zu\n", noLeadingOnesCount);
	printf("Leading 1s: 1........%15zu\n", oneLeadingOneCount);
	printf("Leading 1s: 2........%15zu\n", twoLeadingOnesCount);
	printf("Leading 1s: 3........%15zu\n", threeLeadingOnesCount);
	printf("Leading 1s: 4........%15zu\n", fourLeadingOnesCount);
	printf("Leading 1s: 5........%15zu\n", fiveLeadingOnesCount);
	printf("Leading 1s: 6........%15zu\n", sixLeadingOnesCount);
	printf("Leading 1s: 7........%15zu\n", sevenLeadingOnesCount);
	puts("");

	// Iterate over binary file to read each byte at a time
	totalByteCounter = 0;
	while (fileReadResult = fread(&byte, 1, 1, integersFilePtr) == 1) {
		//Clear the total byte string if this is the start of a new byte
		if (totalByteCounter % 4 == 0) {
			clearString(allBytesCombinedString);
			totalByteCounter = 0;
		}
		//Clear the single byte string and then convert the byte to its base 2 representation
		clearString(convertedByteString);
		convertToNewBase(byte, convertedByteString);

		//Append the single byte onto the total byte string
		size_t allBytesCombinedStringIndex = strlen(allBytesCombinedString);
		for (size_t i = 0; i < strlen(convertedByteString); i++) {
			allBytesCombinedString[allBytesCombinedStringIndex] = convertedByteString[i];
			allBytesCombinedStringIndex++;
		}

		totalByteCounter++;
		// If this is the fourth byte from the file we will convert it to base 10 and see what the value is
		if (totalByteCounter % 4 == 0) {
			singleNum = convertToBaseTen(allBytesCombinedString);
			// Depending on the base 10 value it will create the utf-8 encoded string based on how many bytes it needs to create
			// This will also write the value to a file.
			if (singleNum < 128) {
				createUtfEightString(allBytesCombinedString, 1, integersOutputFilePtr);
			}
			else if (singleNum >= 128 && singleNum < 2048) {
				createUtfEightString(allBytesCombinedString, 2, integersOutputFilePtr);
			}
			else if (singleNum >= 2048 && singleNum < 65536) {
				createUtfEightString(allBytesCombinedString, 3, integersOutputFilePtr);
			}
			else if (singleNum >= 65536 && singleNum < 2097152) {
				createUtfEightString(allBytesCombinedString, 4, integersOutputFilePtr);
			}
			else if (singleNum >= 2097152 && singleNum < 67108864) {
				createUtfEightString(allBytesCombinedString, 5, integersOutputFilePtr);
			}
			else if (singleNum >= 67108864 && singleNum < 2147483648) {
				createUtfEightString(allBytesCombinedString, 6, integersOutputFilePtr);
			}
			else if (singleNum >= 2147483648 && singleNum < 68719476735) {
				createUtfEightString(allBytesCombinedString, 7, integersOutputFilePtr);
			}
			else {
				puts("You made a mistake somewhere");
			}
		}
	}
	fclose(integersFilePtr);
	fclose(integersOutputFilePtr);

	return 0;
}


void createUtfEightString(char* combinedString, const size_t numBytes, FILE* fileOutput) {
	char tempCompleteString[MAX_NUMBER_LENGTH] = { '\0' };

	for (size_t i = 0; i < strlen(combinedString); i++) {
		combinedString[i] = combinedString[i];
	}


	if (numBytes != 1) {
		size_t bitsAdded = 0;
		size_t tempCompleteStringIndex = 0;
		reverseString(combinedString);
		//Create the follow on bytes
		for (size_t i = 0; i < strlen(combinedString); ++i) {
			if (bitsAdded % 6 == 0 && bitsAdded != 0) {
				tempCompleteString[tempCompleteStringIndex] = '0';
				tempCompleteString[tempCompleteStringIndex + 1] = '1';
				tempCompleteStringIndex += 2;
			}
			if (bitsAdded == 6 * (numBytes - 1)) {
				i = strlen(combinedString);
			}
			else {
				tempCompleteString[tempCompleteStringIndex] = combinedString[i];
				tempCompleteStringIndex++;
				bitsAdded++;
			}
		}
		//Shift value to the left the amount of bits that were taken
		for (size_t i = 0; i < strlen(combinedString); i++) {
			combinedString[i] = combinedString[i + bitsAdded];
		}

		// Create initial byte
		for (size_t i = 0; i < 8 - (numBytes + 1); i++) {
			tempCompleteString[strlen(tempCompleteString)] = combinedString[i];
		}
		tempCompleteString[strlen(tempCompleteString)] = '0';
		for (size_t i = 0; i < numBytes; i++) {
			tempCompleteString[strlen(tempCompleteString)] = '1';
		}
	}
	reverseString(tempCompleteString);
	//Break the string into different bytes and write them to a file
	char tempByte[9] = { '\0' };
	uint8_t numToWrite = 0;
	for (size_t iteratorNum = 0; iteratorNum < numBytes; iteratorNum++) {
		for (size_t i = 0; i < 8; i++) {
			tempByte[i] = tempCompleteString[i];
		}
		for (size_t i = 0; i < strlen(tempCompleteString); i++) {
			tempCompleteString[i] = tempCompleteString[i + 8];
		}
		numToWrite = convertToBaseTen(tempByte);
		fwrite(&numToWrite, sizeof(uint8_t), 1, fileOutput);

	}

}


void checkLeadingOnes(const char* convertedByteString, size_t *noLeadingOnesCount, size_t *oneLeadingOneCount, size_t *twoLeadingOnesCount, size_t *threeLeadingOnesCount, size_t *fourLeadingOnesCount, size_t *fiveLeadingOnesCount, size_t *sixLeadingOnesCount, size_t *sevenLeadingOnesCount) {
	if (convertedByteString[0] == '1' && convertedByteString[1] != '1') {
		*oneLeadingOneCount += 1;
	}
	else if (convertedByteString[0] == '1' && convertedByteString[1] == '1' && convertedByteString[2] != '1') {
		*twoLeadingOnesCount += 1;
	}
	else if (convertedByteString[0] == '1' && convertedByteString[1] == '1' && convertedByteString[2] == '1' && convertedByteString[3] != '1') {
		*threeLeadingOnesCount += 1;
	}
	else if (convertedByteString[0] == '1' && convertedByteString[1] == '1' && convertedByteString[2] == '1' && convertedByteString[3] == '1' && convertedByteString[4] != '1') {
		*fourLeadingOnesCount += 1;
	}
	else if (convertedByteString[0] == '1' && convertedByteString[1] == '1' && convertedByteString[2] == '1' && convertedByteString[3] == '1' && convertedByteString[4] == '1' && convertedByteString[5] != '1') {
		*fiveLeadingOnesCount += 1;
	}
	else if (convertedByteString[0] == '1' && convertedByteString[1] == '1' && convertedByteString[2] == '1' && convertedByteString[3] == '1' && convertedByteString[4] == '1' && convertedByteString[5] == '1' && convertedByteString[6] != '1') {
		*sixLeadingOnesCount += 1;
	}
	else if (convertedByteString[0] == '1' && convertedByteString[1] == '1' && convertedByteString[2] == '1' && convertedByteString[3] == '1' && convertedByteString[4] == '1' && convertedByteString[5] == '1' && convertedByteString[6] == '1' && convertedByteString[7] != '1') {
		*sevenLeadingOnesCount += 1;
	}
	else {
		*noLeadingOnesCount += 1;
	}
}


void convertToNewBase(const long number, char* finalString) {
	clearString(finalString);
	long longNumber = 0;
	long startingNumber = number;
	long quotient = 0;
	int remainder = 0;
	int index = 0;
	char fullNumberString[MAX_NUMBER_LENGTH] = { '\0' };


	do {
		char stringValue[2] = { '\0' };
		quotient = startingNumber / 2;
		remainder = startingNumber % 2;
		startingNumber = quotient;
		stringValue[0] = remainder + '0';

		fullNumberString[index] = stringValue[0];
		index++;
	} while (startingNumber != 0);
	
	reverseString(fullNumberString);

	for (size_t i = 0; i < strlen(fullNumberString); i++) {
		finalString[i] = fullNumberString[i];
	}

	if (strlen(finalString) != 8) {
		addZerosToFront(finalString);
	}
}


void reverseString(char* string) {
	char tempString[MAX_NUMBER_LENGTH] = { '\0' };
	size_t length = strlen(string);

	for (size_t i = 0; i < strlen(string); i++) {
		tempString[i] = string[i];
	}
	for (size_t i = 0; i < strlen(string); i++) {
		string[i] = tempString[length - 1 - i];
	}

}


int returnByteCounter(const char* convertedString) {
	int numBytes = 0;

	if (convertedString[0] == '1' && convertedString[1] != '1') {
		puts("Shouldn't be executing because a single leading 1 is a continuation of a number and cannot be the leading byte in UTF-8");
	}
	else if (convertedString[0] == '1' && convertedString[1] == '1' && convertedString[2] != '1') {
		numBytes = 2;
	}
	else if (convertedString[0] == '1' && convertedString[1] == '1' && convertedString[2] == '1' && convertedString[3] != '1') {
		numBytes = 3;
	}
	else if (convertedString[0] == '1' && convertedString[1] == '1' && convertedString[2] == '1' && convertedString[3] == '1' && convertedString[4] != '1') {
		numBytes = 4;
	}
	else if (convertedString[0] == '1' && convertedString[1] == '1' && convertedString[2] == '1' && convertedString[3] == '1' && convertedString[4] == '1' && convertedString[5] != '1') {
		numBytes = 5;
	}
	else if (convertedString[0] == '1' && convertedString[1] == '1' && convertedString[2] == '1' && convertedString[3] == '1' && convertedString[4] == '1' && convertedString[5] == '1' && convertedString[6] != '1') {
		numBytes = 6;
	}
	else if (convertedString[0] == '1' && convertedString[1] == '1' && convertedString[2] == '1' && convertedString[3] == '1' && convertedString[4] == '1' && convertedString[5] == '1' && convertedString[6] == '1' && convertedString[7] != '1') {
		numBytes = 7;
	}
	else {
		numBytes = 1;
	}

	return numBytes;
}


void addZerosToFront(char* string) {
	size_t zerosToAdd = 8 - strlen(string);
	for (int i = strlen(string) - 1; i >= 0; i--) {
		string[i + zerosToAdd] = string[i];
	}
	for (size_t i = 0; i < zerosToAdd; i++) {
		string[i] = '0';
	}
}


uint64_t convertToBaseTen(const char* number) {
	uint64_t longNumber = 0;
	int tempPower = strlen(number) - 1;

	for (size_t i = 0; i < strlen(number); i++) {
		int value = number[i];
		value = value - '0';
		longNumber += (long)value * pow(2, tempPower - i);
	}

	return longNumber;
}


void clearString(char* string) {
	for (int i = MAX_NUMBER_LENGTH - 1; i >= 0; i--) {
		string[i] = '\0';
	}
}


void removeUselessBits(char* string) {
	char tempString[MAX_NUMBER_LENGTH] = { '\0' };
	size_t shiftCounter = 0;
	size_t index = 0;
	while (string[index] == '1') {
		shiftCounter++;
		index++;
	}
	for (size_t i = strlen(string); i > 7; i--) {
		if (string[i] == '1' && string[i + 1] == '0' && i % 8 == 0) {
			shiftLeftTwo(string, i);
		}
	}
	
	//Remove the first byte # identifiers from the frirst byte
	if (shiftCounter > 0) {
		shiftCounter++;
		size_t iterateToIndex = strlen(string) - shiftCounter - 1;

		for (size_t i = 0; i < strlen(string) - shiftCounter; i++) {
			string[i] = string[i + shiftCounter];
		}
		for (size_t i = strlen(string); i > iterateToIndex; i--) {
			string[i] = '\0';
		}
	}
}


void shiftLeftTwo(char* string, const size_t currentIndex) {
	for (size_t i = currentIndex; i < strlen(string); i++) {
		string[i] = string[i + 2];
	}
}


void removeLeadingZeros(char* string) {
	size_t amountToShift = 0;
	bool oneFound = false;
	for (size_t i = 0; i < strlen(string); i++) {
		if (string[i] == '1' && !oneFound) {
			amountToShift = i;
			oneFound = true;
		}
	}
	for (size_t i = 0; i < strlen(string); i++) {
		string[i] = string[i + amountToShift];
	}
}