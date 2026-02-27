/*
  =========================================================================
  PROGRAMMER:..... Joe M. Weibel
  FILE NAME:...... assemble.c
  ASSIGNMENT:..... PJ01
  PROBLEM:........ C
  DUE DATE:....... 13 OCT 2024
  COURSE:......... CS-2160
  SECTION:........ 001
  SEMESTER:....... Fall 2024
  =========================================================================
*/

#define LINE_SIZE 1024
#define MAX_FILE_NAME 1024
#define MAX_EXTENSION 10
#define BINARY_LINE_LENGTH 18
#define BYTE_ARRAY_LENGTH 10
#define BYTE_SIZE 2

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <math.h>

size_t globalRamPosition = 16;

void getFileName(char* file_name);
void removeNewline(char* array);
void firstPass(const char* fileName, const char* parsedFileName, const char* symbolTableFileName);
void secondPass(const char* fileName, const char* bigEndianFileName, const char* littleEndianFileName, const char* hackFileName, const char* symbolTableFileName);
void parseCInstruction(char* line, char* parsedLine);
void convertToLittleEndian(char* lineToConvert);
void parseAInstruction(char* line, char* parsedLine, const char* symbolTableFileName);
bool checkIfAllDigits(char* line);
void convertDecimalToBinary(const char* line, char* parsedLine);
void convertBinaryLineToASCII(const char* binaryLine, unsigned char* firstByte, unsigned char* secondByte);
void checkSymbolTable(const char* line, const char* symbolTableFileName, char* parsedLine);
void generateNewFileName(const char* baseFileName, char* newFileName, char* extension);
void clearLine(char* line);


int main(int argc, char *argv[]) {
	// Setup file names and extension to be modified based on the base file name
	char littleEndianExtension[] = ".hmcl";
	char littleEndianFileName[MAX_FILE_NAME] = { '\0' };
	char bigEndianExtension[] = ".hmcb";
	char bigEndianFileName[MAX_FILE_NAME] = { '\0' };
	char hackExtension[] = ".hack";
	char hackFileName[MAX_FILE_NAME] = { '\0' };
	char symbolTableExtension[] = ".sym";
	char symbolTableFileName[MAX_FILE_NAME] = { '\0' };
	char assemblyFileName[] = "temp_file_to_write.asm";
	char file_name[MAX_FILE_NAME] = { '\0' };
	char baseFileName[MAX_FILE_NAME] = { '\0' };

	// Section of code will see if there was a cmd line argument that is a code file
	// If there was no cmd line argument it will use getFileName() to return a file name to read from
	// The base file name will be used to generate the new file names
	if (argc != 2) {
		getFileName(file_name);
		for (size_t i = 0; i < strlen(file_name); i++) {
			if (file_name[i] == '.') {
				i = strlen(file_name);
			}
			baseFileName[i] = file_name[i];
		}
	}
	else {
		for (size_t i = 0; i < strlen(argv[1]); i++) {
			if (argv[1][i] == '.') {
				i = strlen(argv[1]);
			}
			baseFileName[i] = argv[1][i];
		}

		for (size_t i = 0; i < strlen(argv[1]); i++) {
			file_name[i] = argv[1][i];
		}
	}
	// Generate new file names based on the base file name
	// This expects *char to be passed in for the new file names, extension, and base file name
	// No return value and will modify the passed in *char
	generateNewFileName(baseFileName, littleEndianFileName, littleEndianExtension);
	generateNewFileName(baseFileName, bigEndianFileName, bigEndianExtension);
	generateNewFileName(baseFileName, hackFileName, hackExtension);
	generateNewFileName(baseFileName, symbolTableFileName, symbolTableExtension);

	// Broke the program into two functions to handle the first and second pass
	// The first pass will remove all whitespace, comments, and labels and create the intial symbol table
	// The second pass will convert the assembly code to binary and write to a file
	firstPass(file_name, assemblyFileName, symbolTableFileName);
	secondPass(assemblyFileName, bigEndianFileName, littleEndianFileName, hackFileName, symbolTableFileName);

}


void getFileName(char* file_name) {
	printf("Enter the file name: ");
	fgets(file_name, MAX_FILE_NAME, stdin);
	removeNewline(file_name);
}


void removeNewline(char* array) {
	//Checking if the last index of the string length is newline, and changing it to null terminator
	if (array[strlen(array) - 1] == '\n') {
		array[strlen(array) - 1] = '\0';
	}
}


void firstPass(const char* baseFileName, const char* parsedFileName, const char* symbolTableFileName) {
	FILE* file = fopen(baseFileName, "r");
	FILE* output = fopen("projectFirstPass.asm", "w");

	if (file == NULL) {
		printf("Error opening file %s\n", baseFileName);
	}
	else {
		char line[LINE_SIZE] = { '\0' };


		// This loop reads the file line by line and removes all whitespace characters
		// The file to be read from and file to be wrote to will be closed after this loop
		// This will write the temp file with no whitespace "prjectFirstPass.asm" and will be later deleted when no longer needed
		while (fgets(line, sizeof(line), file)) {
			char newLine[LINE_SIZE] = { '\0' };
			size_t j = 0;

			for (size_t i = 0; line[i] != '\0'; i++) {
				if (i == 0 && line[i] == '\n') {
					line[i] = '\0';
				}
				else {
					if (line[i] != ' ') {
						newLine[j++] = line[i];
					}
				}
			}
			newLine[j + 1] = '\0';

			fprintf(output, "%s", newLine);
		}
		fclose(file);
		fclose(output);

		//This loop reads the file that was just written and removes comments
		// Will check if two consecutive indexes in the line are '/' and '/' and will nullify the remainder of the line
		// This will take in the file that was just written and remove all comments and write to a new file "projectNoComments.asm"
		// AFter this loop we should close and remove the whitepsace temp file and the file with no comments will be used for the next loop
		FILE* removeCommentsFile = fopen("projectFirstPass.asm", "r");
		FILE* noCommentsFile = fopen("projectNoComments.asm", "w");
		char removeCommentLine[LINE_SIZE] = {'\0'};

		while (fgets(removeCommentLine, sizeof(removeCommentLine), removeCommentsFile)) {
			for (size_t i = 0; removeCommentLine[i] != '\0'; i++) {
				if (removeCommentLine[i] == '/' && removeCommentLine[i+1] == '/') {
					removeCommentLine[i] = '\n';
					for (size_t j = i+1; j < sizeof(removeCommentLine); j++) {
						removeCommentLine[j] = '\0';
					}
				}
			}
			if (removeCommentLine[0] != '\n') {
				fprintf(noCommentsFile, "%s", removeCommentLine);
			}
		}
		fclose(removeCommentsFile);
		remove("projectFirstPass.asm");
		fclose(noCommentsFile);


		// This loop reads the file that was just written and removes all labels and creates a symbol table
		// Will check if the first character in the line is '(' and the last character is ')' and will remove the line
		// Along with removing the line that contains the parenthesis it will place that label in the symbol table associated with the line number it resides on as the memory address
		// This will take in the file that was just written and remove all labels and write to a new file "projectNoComments.asm"
		// This will also create the symbol table and write to a new file "symbolTableFileName"
		// After this loop we should close and remove the file with no comments and the file with no labels will be used for the next loop
		FILE* removeLabelsFile = fopen("projectNoComments.asm", "r");
		FILE* noLabelsFile = fopen(parsedFileName, "w");
		FILE* symbolTable = fopen(symbolTableFileName, "w");
		char removeLabelLine[LINE_SIZE] = { '\0' };
		char label[LINE_SIZE] = { '\0' };

		// Standard values to initialize symbol table
		fprintf(symbolTable, "========================\n");
		fprintf(symbolTable, "PRE-DEFINED SYMBOLS\n");
		fprintf(symbolTable, "========================\n");
		fprintf(symbolTable, "Symbol   Address   Used\n");
		for (int i = 0; i < 16; i++) {
			fprintf(symbolTable, "R%-8d%7d   false\n", i, i);
		}
		fprintf(symbolTable, "SCREEN     16384   false\n");
		fprintf(symbolTable, "KBD        24576   flase\n");
		fprintf(symbolTable, "SP             0   false\n");
		fprintf(symbolTable, "LCL            1   false\n");
		fprintf(symbolTable, "ARG            2   false\n");
		fprintf(symbolTable, "THIS           3   false\n");
		fprintf(symbolTable, "THAT           4   false\n\n");

		fprintf(symbolTable, "========================\n");
		fprintf(symbolTable, "USER-DEFINED SYMBOLS\n");
		fprintf(symbolTable, "========================\n");
		fprintf(symbolTable, "Symbol   Address   Used\n");

		int lineNumber = 1;
		size_t j = 0;
		size_t lineLength = 0;
		// This loop will pull the user defined symbols
		while (fgets(removeLabelLine, sizeof(removeLabelLine), removeLabelsFile)) {
			j = 0;
			lineLength = strlen(removeLabelLine);

			if (removeLabelLine[0] == '(' && (removeLabelLine[lineLength - 1] == ')' || removeLabelLine[lineLength - 2] == ')')) {
				for (int i = (int)strlen(label); i >= 0; i--) {
					label[i] = '\0';
				}
				for (size_t i = 1; i < (int)strlen(removeLabelLine) - 1; i++) {
					if (removeLabelLine[i] != ')') {
						label[j] = removeLabelLine[i];
						j++;
					}
				}
				for (int i = (int)strlen(removeLabelLine); i >= 0; i--) {
					removeLabelLine[i] = '\0';
				}
				fprintf(symbolTable, "%-8s %7d    true\n", label, lineNumber);
			}

			if (removeLabelLine[0] != '\n') {
				fprintf(noLabelsFile, "%s", removeLabelLine);
			}
			lineNumber++;
		}
		fprintf(symbolTable, "\n========================\n");
		fprintf(symbolTable, "NAMED VARIABLES\n");
		fprintf(symbolTable, "========================\n");
		fprintf(symbolTable, "Variable  Address   Used\n");

		fclose(removeLabelsFile);
		remove("projectNoComments.asm");
		fclose(noLabelsFile);
		fclose(symbolTable);
	}
}


void secondPass(const char* fileName, const char* bigEndianFileName, const char* littleEndianFileName, const char* hackFileName, const char* symbolTableFileName) {
	// The parsed file with no comments, whitespace, or labels is in fileName char[] and will be read from
	// The big and little endian files will be opened in wb for writing binary values
	FILE* file = fopen(fileName, "r");
	FILE* outputBigEndian = fopen(bigEndianFileName, "wb");
	FILE* outputLittleEndian = fopen(littleEndianFileName, "wb");
	FILE* project = fopen(hackFileName, "w");
	char line[LINE_SIZE] = { '\0' };
	char binaryLine[BINARY_LINE_LENGTH] = { '\0' };

	if (file == NULL || outputBigEndian == NULL || outputLittleEndian == NULL || project == NULL) {
		printf("Error opening a file for second pass\n");
	}
	else {
		while (fgets(line, sizeof(line), file)) {
			if (line[0] == '@') {
				// Parse the A instruction and write the binary line to text file
				parseAInstruction(line, binaryLine, symbolTableFileName);
				fprintf(project, "%s", binaryLine);
			}
			else {
				// Parse the C instruction and write the binary line to text file
				parseCInstruction(line, binaryLine);
				fprintf(project, "%s", binaryLine);
			}
			// Convert binary line to ASCII and write to binary file EXTRA CREDIT
			// Initialize unsigned char variables to hold the byte addresses
			// convertBinaryLineToASCII will take in the line to parse, and two bytes to modify, no return value
			// This will read the binary line, get the integer values, place those integer values in the address of the unsigned char
			unsigned char firstByte[BYTE_SIZE] = { '\0' };
			unsigned char secondByte[BYTE_SIZE] = { '\0' };
			convertBinaryLineToASCII(binaryLine, firstByte, secondByte);

			// This is simple logic to write the unsigned char to a binary file in big endian by writing the first byte and then the second byte
			// The reverse occurs for the little endian file
            fwrite(&firstByte[0], sizeof(unsigned char), strlen(firstByte), outputBigEndian);
			fwrite(&secondByte[0], sizeof(unsigned char), strlen(secondByte), outputBigEndian);
			fwrite(&secondByte[0], sizeof(unsigned char), strlen(secondByte), outputLittleEndian);
			fwrite(&firstByte[0], sizeof(unsigned char), strlen(firstByte), outputLittleEndian);
		}
		fclose(file);
		remove("temp_file_to_write.asm");
		fclose(outputBigEndian);
		fclose(outputLittleEndian);
		fclose(project);
	}
}


void parseCInstruction(char* line, char* parsedLine) {
	char destBits[LINE_SIZE] = { '\0' };
	destBits[0] = '0';
	destBits[1] = '0';
	destBits[2] = '0';
	char compBits[LINE_SIZE] = { '\0' };
	compBits[0] = '0';
	compBits[1] = '0';
	compBits[2] = '0';
	compBits[3] = '0';
	compBits[4] = '0';
	compBits[5] = '0';
	char jumpBits[LINE_SIZE] = { '\0' };
	jumpBits[0] = '0';
	jumpBits[1] = '0';
	jumpBits[2] = '0';

	char cInstructionPrefix[4] = { '1', '1', '1', '\0' };
	char aBit[LINE_SIZE] = { '0', '\0' };
	size_t equalsIndex = 0;

	for (size_t i = 0; i < strlen(line) - 1; i++) {
		if (line[i] == '=') {
			equalsIndex = i;
			// Working with left of = and will create dest bits
			for (size_t j = 0; j < i; j++) {
				if (line[j] == 'A') {
					destBits[0] = '1';
				}
				else if (line[j] == 'D') {
					destBits[1] = '1';
				}
				else if (line[j] == 'M') {
					destBits[2] = '1';
				}
			}
			destBits[3] = '\0';
		}
		else if (line[i] == ';') {
			//Working with right of ; and will create jump bits
			if (line[strlen(line)-3] == 'G' && line[strlen(line) - 2] == 'T') {
				jumpBits[2] = '1';
			}
			else if (line[strlen(line) - 3] == 'E' && line[strlen(line) - 2] == 'Q') {
				jumpBits[1] = '1';
			}
			else if (line[strlen(line) - 3] == 'G' && line[strlen(line) - 2] == 'E') {
				jumpBits[1] = '1';
				jumpBits[2] = '1';
			}
			else if (line[strlen(line) - 3] == 'L' && line[strlen(line) - 2] == 'T') {
				jumpBits[0] = '1';
			}
			else if (line[strlen(line) - 3] == 'N' && line[strlen(line) - 2] == 'E') {
				jumpBits[0] = '1';
				jumpBits[2] = '1';
			}
			else if (line[strlen(line) - 3] == 'L' && line[strlen(line) - 2] == 'E') {
				jumpBits[0] = '1';
				jumpBits[1] = '1';
			}
			else {
				jumpBits[0] = '1';
				jumpBits[1] = '1';
				jumpBits[2] = '1';
			}
			jumpBits[3] = '\0';
		}
	}
	// Create bit string for computation bits
	char computation[10] = { '\0' };
	size_t index = 0;
	while (equalsIndex < strlen(line) - 1 && line[equalsIndex] != ';' && line[equalsIndex] != '\n') {
		if (line[equalsIndex] != '=') {
			computation[index] = line[equalsIndex];
			index++;
		}
		equalsIndex++;
	}
	// Set a bit if M is in computation
	for (size_t i = 0; i < strlen(computation); i++) {
		if (computation[i] == 'M') {
			aBit[0] = '1';
		}
	}

	// A series of if, else it conditions to determine what the string should be based on the bits that are set
	// This is based off the ALU computations available based on the A|M computations
	if (computation[0] == '0') {
		compBits[0] = '1';
		compBits[2] = '1';
		compBits[4] = '1';
	}
	else if (computation[0] == '1') {
		compBits[0] = '1';
		compBits[1] = '1';
		compBits[2] = '1';
		compBits[3] = '1';
		compBits[4] = '1';
		compBits[5] = '1';
	}
	else if (computation[0] == '-' && computation[1] == '1') {
		compBits[0] = '1';
		compBits[1] = '1';
		compBits[2] = '1';
		compBits[4] = '1';
	}
	else if (computation[0] == 'D') {
		compBits[2] = '1';
		compBits[3] = '1';
	}
	else if ((computation[0] == 'A' || computation[0] == 'M') && computation[1] == '\0') {
		compBits[0] = '1';
		compBits[1] = '1';
	}
	else if (computation[0] == '!' && computation[1] == 'D') {
		compBits[2] = '1';
		compBits[3] = '1';
		compBits[5] = '1';
	}
	else if (computation[0] == '!' && (computation[1] == 'A' || computation[1] == 'M')) {
		compBits[0] = '1';
		compBits[1] = '1';
		compBits[5] = '1';
	}
	else if (computation[0] == '-' && computation[1] == 'D') {
		compBits[2] = '1';
		compBits[3] = '1';
		compBits[4] = '1';
		compBits[5] = '1';
	}
	else if (computation[0] == '-' && (computation[1] == 'A' || computation[1] == 'M')) {
		compBits[0] = '1';
		compBits[1] = '1';
		compBits[4] = '1';
		compBits[5] = '1';
	}
	else if (computation[0] == 'D' && computation[1] == '+' && computation[2] == '1') {
		compBits[1] = '1';
		compBits[2] = '1';
		compBits[3] = '1';
		compBits[4] = '1';
		compBits[5] = '1';
	}
	else if ((computation[0] == 'A' || computation[0] == 'M') && computation[1] == '+' && computation[2] == '1') {
		compBits[0] = '1';
		compBits[1] = '1';
		compBits[3] = '1';
		compBits[4] = '1';
		compBits[5] = '1';
	}
	else if (computation[0] == 'D' && computation[1] == '-' && computation[2] == '1') {
		compBits[2] = '1';
		compBits[3] = '1';
		compBits[4] = '1';
	}
	else if ((computation[0] == 'A' || computation[0] == 'M') && computation[1] == '-' && computation[2] == '1') {
		compBits[0] = '1';
		compBits[1] = '1';
		compBits[4] = '1';
	}
	else if (computation[0] == 'D' && computation[1] == '+' && (computation[2] == 'A' || computation[2] == 'M')) {
		compBits[4] = '1';
	}
	else if (computation[0] == 'D' && computation[1] == '-' && (computation[2] == 'A' || computation[2] == 'M')) {
		compBits[1] = '1';
		compBits[4] = '1';
		compBits[5] = '1';
	}
	else if ((computation[0] == 'A' || computation[0] == 'M') && computation[1] == '-' && computation[2] == 'D') {
		compBits[5] = '3';
		compBits[5] = '4';
		compBits[5] = '5';
	}
	else if (computation[0] == 'D' && computation[1] == '|' && (computation[2] == 'A' || computation[2] == 'M')) {
		compBits[1] = '1';
		compBits[3] = '1';
		compBits[5] = '1';
	}
	compBits[6] = '\0';

	// Construct full C instruction
	// Will increment index separetely to track the index of the parsedLine
	index = 0;
	clearLine(parsedLine);
	for (size_t i = 0; i < strlen(cInstructionPrefix); i++) {
		parsedLine[index] = cInstructionPrefix[i];
		index++;
	}
	for (size_t i = 0; i < strlen(aBit); i++) {
		parsedLine[index] = aBit[i];
		index++;
	}
	for (size_t i = 0; i < strlen(compBits); i++) {
		parsedLine[index] = compBits[i];
		index++;
	}
	for (size_t i = 0; i < strlen(destBits); i++) {
		parsedLine[index] = destBits[i];
		index++;
	}
	for (size_t i = 0; i < strlen(jumpBits); i++) {
		parsedLine[index] = jumpBits[i];
		index++;
	}
	parsedLine[index] = '\n';
}


void convertToLittleEndian(char* lineToConvert) {
	// Will move ast 8 bits to the front of the line
	// ill move the last 8 bits to the back of the line
	// This will be used to convert the binary line to little endian
	char temp[9] = { '\0' };
	size_t tempIndex = 0;

	for (size_t i = 0; i < strlen(lineToConvert) / 2; i++) {
		temp[i] = lineToConvert[i];
	}

	for (size_t i = 0; i < strlen(lineToConvert) / 2; i++) {
		lineToConvert[i] = lineToConvert[i+8];
	}

	for (size_t i = 8; i < strlen(lineToConvert) - 2; i++) {
		lineToConvert[i] = temp[tempIndex];
		tempIndex++;
	}
}


void parseAInstruction(char* line, char* parsedLine, const char* symbolTableFileName) {
	// If the A instruction is all digits we just need to load the value into memory
	// This function jsut takes in the current line and will check each character for a letter
	bool allDigits = checkIfAllDigits(line);

	if (allDigits) {
		// The return value of allDigits() will be used to decide how to parse the line
		// This will be executed if every character in the line after '@' is a digit
		convertDecimalToBinary(line, parsedLine);
		
	}
	else {
		// This function will check the symbol table to see if the variable is already in the table
		// IF the function is in the symbol table it will return the binary line for the memory address
		// Else the function will add the variable to the symbol table and return the binary line for the next available memory address
		checkSymbolTable(line, symbolTableFileName, parsedLine);
	}
}


bool checkIfAllDigits(char* line) {
	// Defaults to being true, if a non-digit character is found the value will be set to false and returned
	// Using while loop so the loop can terminate if it finds a value that is not a digit
	// Strting at index 1 becase '@' is the first character in the line
	bool allDigits = true;
	size_t index = 1;

	while (allDigits && index < strlen(line) - 1) {
		if (!isdigit(line[index])) {
			allDigits = false;
		}
		index++;
	}
	return allDigits;
}


void convertDecimalToBinary(const char* line, char* parsedLine) {
	char tempLine[LINE_SIZE] = { '\0' };
	// Shift line 1 to the left to remove the '@' character
	// This will be used to convert the string value to an integer using atoi()
	if (line[0] == '@') {
		for (size_t i = 0; i < strlen(line); i++) {
			tempLine[i] = line[i + 1];
		}
	}
	else {
		for (size_t i = 0; i < strlen(line); i++) {
			tempLine[i] = line[i];
		}
	}
	int decimal = 0;
	// Set 16 values to 0
	for (size_t i = 0; i < BINARY_LINE_LENGTH - 2; i++) {
		parsedLine[i] = '0';
	}
	// Ensure newline and null termination of the line
	parsedLine[BINARY_LINE_LENGTH - 2] = '\n';
	parsedLine[BINARY_LINE_LENGTH - 1] = '\0';

	// Convert decimal to binary
	decimal = atoi(tempLine);
	int index = BINARY_LINE_LENGTH - 3;
	while (decimal > 0) {
		if (decimal % 2 != 0) {
			parsedLine[index] = '1';
		}
		decimal = decimal / 2;
		index--;
	}
}


void convertBinaryLineToASCII(const char* binaryLine, unsigned char* firstByte, unsigned char* secondByte) {
	int firstByteInt = 0;
	int secondByteInt = 0;
	size_t byteArraySize = (strlen(binaryLine) - 1) / 2;
	size_t indexTracker = 0;

	// Get integer value of first 8 bits
	for (int i = (int)byteArraySize - 1; i >= 0; i--) {
		if (binaryLine[i] == '1') {
			firstByteInt +=  (int)round(pow(2, indexTracker));
		}
		indexTracker++;
	}

	// Get integer value of last 8 bits
	indexTracker = 0;
	for (size_t i = (size_t)byteArraySize + byteArraySize - 1; i >= (size_t)byteArraySize; i--) {
		if (binaryLine[i] == '1') {
			secondByteInt += (int)round(pow(2, indexTracker));
		}
		indexTracker++;
	}
	*firstByte = firstByteInt;
	*secondByte = secondByteInt;
}


void checkSymbolTable(const char* line, const char* symbolTableFileName, char* parsedLine) {
	// Create temp var and copy line into temp line so we dont modify the original line
	// Simultaneously remove the '@' and newline character
	char tempLine[LINE_SIZE] = { '\0' };
	for (size_t i = 1; i < strlen(line); i++) {
		tempLine[i-1] = line[i];
	}
	tempLine[strlen(tempLine)-1] = ' ';

	FILE* symbolTable = fopen(symbolTableFileName, "r");
	FILE* tempSymbolTable = fopen("tempSymbolTable.sym", "w");
	char searchLine[LINE_SIZE] = { '\0' };
	long int lineStart = 0;
	bool matchFound = false;
	bool stringFoundInFile = false;

	while (fgets(searchLine, sizeof(searchLine), symbolTable)) {

		if (strstr(searchLine, tempLine) != NULL) {
			matchFound = true;
			stringFoundInFile = true;
			tempLine[strlen(tempLine) - 1] = '\0';
			char address[10] = { '\0' };
			size_t index = 0;

			for (size_t i = strlen(tempLine); i < strlen(searchLine); i++) {
				if (isdigit(searchLine[i])) {
					address[index] = searchLine[i];
					index++;
				}
			}

			// Write new line to file
			fprintf(tempSymbolTable, "%-8s %7s    true\n", tempLine, address);

			convertDecimalToBinary(address, parsedLine);
			
		}
		else {
			matchFound = false;
		}
		if (!matchFound) {
			fprintf(tempSymbolTable, "%s", searchLine);
		}

	}
	fclose(symbolTable);
	fclose(tempSymbolTable);
	remove(symbolTableFileName);
	(void)rename("tempSymbolTable.sym", symbolTableFileName);

	// If the variable was not found in the file I need to append it to the NAMED VARIABLES section
	if (!stringFoundInFile) {
		FILE* symbolTable = fopen(symbolTableFileName, "a");
		fprintf(symbolTable, "%-8s %7zu    true\n", tempLine, globalRamPosition);
		fclose(symbolTable);
		char ramCharArray[10] = { '\0' };
		snprintf(ramCharArray, sizeof(ramCharArray), "%zu", globalRamPosition);
		convertDecimalToBinary(ramCharArray, parsedLine);
		globalRamPosition++;
	}
}


void generateNewFileName(const char* baseFileName, char* newFileName, char* extension) {
	size_t length = strlen(baseFileName);
	for (size_t i = 0; i < strlen(baseFileName); i++) {
		newFileName[i] = baseFileName[i];
	}
	for (size_t i = 0; i < strlen(extension); i++) {
		newFileName[i+length] = extension[i];
	}
}


void clearLine(char* line) {
	for (int i = strlen(line); i > 0; i--) {
		line[i] = '\0';
	}
}