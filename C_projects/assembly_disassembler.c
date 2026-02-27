/*
  =========================================================================
  PROGRAMMER:..... Joe M. Weibel
  FILE NAME:...... dehack.c
  ASSIGNMENT:..... PJ01
  PROBLEM:........ B
  DUE DATE:....... 06 OCT 2024
  COURSE:......... CS-2160
  SECTION:........ 001
  SEMESTER:....... Fall 2024
  =========================================================================
*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

#define MAX_FILE_EXTENSION 10
#define MAX_FILE_NAME 100
#define ASSEMBLY_LINE 1024
#define BINARY_LINE_SIZE 2
#define BINARY_LINE_LENGTH 18
#define BYTE_LENGTH 9

void get_file_extension(const char *filename, char *fileExtension, char* fullAsmFile);
void parse_hack_file(char* filename, FILE* asmFile);
void parse_hmc_file(char* filename, FILE* asmFile);
void write_asm_file(FILE* file, const char* lineToWrite);
int convert_binary_to_decimal(const char* binary);
void return_destination_translation(char* destBits, char* asmDestString);
void return_jump_translation(char* jumpBits, char* asmJumpString);
void return_a_translation(char* aBits, char* asmAString);
void return_computation_translation(const char* computationBits, char* computationString, const char* aString);
void create_c_instruction_string(const char* destString, const char* jumpString, const char* compString, char* fullString);
bool check_endianess(FILE* hmcFile);
char* get_file_from_user(char* file);
void removeNewline(char* array);
void convertDecimalToBinary(const int decimalToConvert, char* binaryLine);
void createTempFile(FILE* binaryFilePtr, const char* convertedFileName);
void convertLittleEndianToBigEndian(const char* convertedFileName);
void clearCharArray(char* array);

int main(int argc, char* argv[]) {
	// Initialize all char array variables to null terminator
    char fileExtension[MAX_FILE_EXTENSION] = { '\0' };
    char fileName[MAX_FILE_NAME] = { '\0' };
    char fullAsmFileName[MAX_FILE_NAME] = { '\0' };
	char asmFileExtension[] = ".asm";

	// Get the file name from the user
	// This will check if the program was run with an argument, if not it will prompt the user for a file name
	// I wrote the code this way so I can use the debugger built into the IDE
	if (argc != 2) {
		get_file_from_user(fileName);
	}
	else {
		for (size_t i = 0; i < strlen(argv[1]); i++) {
			fileName[i] = argv[1][i];
		}
	}
	// If no file name is entered, print an error message. Else , get the file extension and create the .asm file
    if (strlen(fileName) < 1) {
        printf("You must enter an argument with a file name");
    }
    else {
		// Description: This function expects three char*. This will return the as file name without an extension for creation later and get the file extension.
        get_file_extension(fileName, fileExtension, fullAsmFileName);
		size_t index = 0;
		// This will add the .asm extension to the base file name
		for (size_t i = strlen(fullAsmFileName); i < (strlen(fullAsmFileName) + strlen(asmFileExtension)) - 3; i++) {
			fullAsmFileName[i] = asmFileExtension[index];
			index++;
		}

		FILE* asmFile = fopen(fullAsmFileName, "w");

		if (asmFile == NULL) {
			printf("Failed to open a file: %s", fullAsmFileName);
		}
		else {
			// Using strvmp to compare the file extension to determine which function to call
			// strcmp() expects two null termindated char arrays and will return 0 if they are equal
			if (strcmp(fileExtension, "hack") == 0) {
				// This block of code is executed if the file extension is "hack"
				fprintf(asmFile, "// File parsed from .hack file\n");
				parse_hack_file(fileName, asmFile);
			}
			else if (strcmp(fileExtension, "hmc") == 0 || strcmp(fileExtension, "hmcl") == 0 || strcmp(fileExtension, "hmcb") == 0) {
				// This block of code is executed if the file extension is "hmc", "hmcl", or "hmcb"
				// This block of code will call necessary functions to determine big or little endian and convert the file to big endian
				// Then this block of code will call parse_hack_file to parse the file with the temp file that contains the big endian ascii text
				fprintf(asmFile, "// File parsed from .hmc file\n");
				parse_hmc_file(fileName, asmFile);
			}
			else {
				// This block of code is executed if the file extension is not "hack" or "hmc"
				printf("Unsupported file extension");
			}
			fclose(asmFile);
		}
    }
    return 0;
}


void get_file_extension(const char* filename, char *fileExtension, char* fullAsmFile) {
	for (size_t i = 0; i < strlen(filename); i++) {
		fullAsmFile[i] = filename[i];
	}
	//strcpy(fullAsmFile, filename);
	int i = 0;
	int j = 0;
	bool found = false;
	// Will iterate until the index is null terminator
	while (filename[i] != '\0') {
		// If the index is a period, it will set found to true and set the fullAsmFile to null terminator
		if (filename[i] == '.') {
			found = true;
			fullAsmFile[i] = '\0';
			i++;
		}
		if (found) {
			// If found is true, it will set the fileExtension to the file extension
			fileExtension[j] = filename[i];
			j++;
			fullAsmFile[i] = '\0';
		}
		i++;
	}
}


void parse_hack_file(char* filename, FILE* asmFile) {
	// This function takes a file pointer and a char* to the base memory address of a char[] that will be the file name to read from
	FILE* file = fopen(filename, "r");
	if (file == NULL) {
		printf("Error opening file %s", filename);
	}
	else {
		char line[ASSEMBLY_LINE] = { '\0' };
		while (fgets(line, sizeof(line), file)) {
			if (strlen(line) < 16) {
				printf("");
			}
			else {
				bool cInstruction = false;

				if (line[0] == '1') {
					// This boolean will determine if I need to interpret the line as '@numeric value' or parse for C instruction
					cInstruction = true;
				}

				if (cInstruction) {
					// Initialize all char[] for bits to NULL terminator
					char asmDestinationString[5] = { '\0' };
					char asmJumpString[ASSEMBLY_LINE] = { '\0' };
					char asmAString[3] = { '\0' };
					char asmComputationString[10] = { '\0' };
					char asemblyLine[ASSEMBLY_LINE] = { '\0' };

					char useARegisterBit[2] = {'\0'};
					char computationBits[7] = { '\0' };
					char destBits[4] = { '\0' };
					char jumpBits[4] = { '\0' };

					useARegisterBit[0] = line[3];
					size_t bitIndex = 0;
					for (size_t i = 4; i < 10; i++) {
						computationBits[bitIndex] = line[i];
						bitIndex++;
					}
					bitIndex = 0;
					for (size_t i = 10; i < 13; i++) {
						destBits[bitIndex] = line[i];
						bitIndex++;
					}
					bitIndex = 0;
					for (size_t i = 13; i < 16; i++) {
						jumpBits[bitIndex] = line[i];
						bitIndex++;
					}

					// These functions will parse each line if it is a C instruction and search for the specific bits and return the correct string for the assembly file
					// These functions all take pointers to the char[] and will modify the char[] to the correct string
					return_destination_translation(destBits, asmDestinationString);
					return_jump_translation(jumpBits, asmJumpString);
					return_a_translation(useARegisterBit, asmAString);
					return_computation_translation(computationBits, asmComputationString, asmAString);
					create_c_instruction_string(asmDestinationString, asmJumpString, asmComputationString, asemblyLine);
					write_asm_file(asmFile, asemblyLine);
					

				}
				else {
					// If it is an A instruction it will convert the binary to decimal and write the line to the assembly file
					int decimal = 0;
					decimal = convert_binary_to_decimal(line);
					char assemblyLine[ASSEMBLY_LINE] = { '\0' };
					snprintf(assemblyLine, sizeof(assemblyLine), "@%d", decimal);
					// Function expects a FILE* and a char* to write to the file
					write_asm_file(asmFile, assemblyLine);
				}
			}
		}
		fclose(file);
	}
}


void parse_hmc_file(char* filename, FILE* asmFile) {
	//Creating a temporary file to write the converted endianess to
	FILE* file = fopen(filename, "rb");
	if (file == NULL) {
		printf("Error opening file %s", filename);
	}
	else {
		// If conditional will return true if the file is little endian
		if (check_endianess(file)) {
			fprintf(asmFile, "// Little Endian\n");
			char binaryFileConvertedName[] = "temp_converted_file.hack";
			createTempFile(file, binaryFileConvertedName);
			// If it is little endian it will modify a temp file and convert the endianess to big endian
			convertLittleEndianToBigEndian(binaryFileConvertedName);
			remove(binaryFileConvertedName);
			// Parse the temp file as normal with parse hack and the remove the temp file
			parse_hack_file("convertedToBigEndianDeleteMe.hack", asmFile);
			remove("convertedToBigEndianDeleteMe.hack");
		}
		else {
			fprintf(asmFile, "// Big Endian\n");
			char binaryFileConvertedName[] = "temp_converted_file.hack";
			createTempFile(file, binaryFileConvertedName);

			// Parse the temp file as normal with parse hack and the remove the temp file
			parse_hack_file(binaryFileConvertedName, asmFile);
			remove(binaryFileConvertedName);
		}
		// Send the temp.hmc to parse_hack_file to parse the file as it is now converted to big endian
		if (check_endianess(file)) {
			parse_hack_file("temp.hmc", asmFile);
		}
		else {
			parse_hack_file(filename, asmFile);
		}
		fclose(file);
	}
}


void write_asm_file(FILE *file, const char *lineToWrite) {
	// If at the beginning of the file it will not write a newline, else it will write a newline
    if (ftell(file) != 0) {
        fprintf(file, "\n");
    }
    fprintf(file, lineToWrite);
}


int convert_binary_to_decimal(const char* binary) {
	// Will us the pow() to take the binary value and convert it to decimal to the power of 2, then type cast to int
	int decimal = 0;
	for (size_t character = strlen(binary) - 1; character > 0; character--) {
		if (binary[character] == '1') {
			size_t binaryLocation = strlen(binary) - 2;
			binaryLocation = binaryLocation - character;
            decimal += (int)pow(2, binaryLocation);
		}
	}
	return decimal;
}


void return_destination_translation(char* destBits, char* asmDestString) {
	// If else conditioanls to determine the destination bits and return the correct string
	if (destBits[0] == '0' && destBits[1] == '0' && destBits[2] == '1') {
		char destString[] = "M=";
		snprintf(asmDestString, sizeof(asmDestString), "%s", destString);
	}
	else if (destBits[0] == '0' && destBits[1] == '1' && destBits[2] == '0') {
		char destString[] = "D=";
		snprintf(asmDestString, sizeof(asmDestString), "%s", destString);
	}
	else if (destBits[0] == '0' && destBits[1] == '1' && destBits[2] == '1') {
		char destString[] = "DM=";
		snprintf(asmDestString, sizeof(asmDestString), "%s", destString);
	}
	else if (destBits[0] == '1' && destBits[1] == '0' && destBits[2] == '0') {
		char destString[] = "A=";
		snprintf(asmDestString, sizeof(asmDestString), "%s", destString);
	}
	else if (destBits[0] == '1' && destBits[1] == '0' && destBits[2] == '1') {
		char destString[] = "AM=";
		snprintf(asmDestString, sizeof(asmDestString), "%s", destString);
	}
	else if (destBits[0] == '1' && destBits[1] == '1' && destBits[2] == '0') {
		char destString[] = "AD=";
		snprintf(asmDestString, sizeof(asmDestString), "%s", destString);
	}
	else if (destBits[0] == '1' && destBits[1] == '1' && destBits[2] == '1') {
		char destString[] = "ADM=";
		snprintf(asmDestString, sizeof(asmDestString), "%s", destString);
	}
	else {
		char destString[] = "";
		snprintf(asmDestString, sizeof(asmDestString), "%s", destString);
	}
}


void return_jump_translation(char* jumpBits, char* asmJumpString) {
	// If else conditionals to determine the jump bits and return the correct string
	if (jumpBits[0] == '0' && jumpBits[1] == '0' && jumpBits[2] == '1') {
		char jumpString[] = ";JGT";
		snprintf(asmJumpString, sizeof(asmJumpString), "%s", jumpString);
	}
	else if (jumpBits[0] == '0' && jumpBits[1] == '1' && jumpBits[2] == '0') {
		char jumpString[] = ";JEQ";
		snprintf(asmJumpString, sizeof(asmJumpString), "%s", jumpString);
	}
	else if (jumpBits[0] == '0' && jumpBits[1] == '1' && jumpBits[2] == '1') {
		char jumpString[] = ";JGE";
		snprintf(asmJumpString, sizeof(asmJumpString), "%s", jumpString);
	}
	else if (jumpBits[0] == '1' && jumpBits[1] == '0' && jumpBits[2] == '0') {
		char jumpString[] = ";JLT";
		snprintf(asmJumpString, sizeof(asmJumpString), "%s", jumpString);
	}
	else if (jumpBits[0] == '1' && jumpBits[1] == '0' && jumpBits[2] == '1') {
		char jumpString[] = ";JNE";
		snprintf(asmJumpString, sizeof(asmJumpString), "%s", jumpString);
	}
	else if (jumpBits[0] == '1' && jumpBits[1] == '1' && jumpBits[2] == '0') {
		char jumpString[] = ";JLE";
		snprintf(asmJumpString, sizeof(asmJumpString), "%s", jumpString);
	}
	else if (jumpBits[0] == '1' && jumpBits[1] == '1' && jumpBits[2] == '1') {
		char jumpString[] = ";JMP";
		snprintf(asmJumpString, sizeof(asmJumpString), "%s", jumpString);
	}
	else {
		char jumpString[] = "";
		snprintf(asmJumpString, sizeof(asmJumpString), "%s", jumpString);
	}
}


void return_a_translation(char* aBits, char* asmAString) {
	// If else conditionals to determine the a bits and return the correct string
	if (aBits[0] == '0') {
		char aString[] = "A";
		snprintf(asmAString, sizeof(asmAString), "%s", aString);
	}
	else {
		char aString[] = "M";
		snprintf(asmAString, sizeof(asmAString), "%s", aString);
	}
}


void return_computation_translation(const char* computationBits, char* computationString, const char* aString) {
	// If else conditionals to determine the computation bits and return the correct string
	if (*aString == 'A') {
		if (computationBits[0] == '0' && computationBits[1] == '0' && computationBits[2] == '0' && computationBits[3] == '0' && computationBits[4] == '0' && computationBits[5] == '0') {
			char computation[] = "D&A";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '1' && computationBits[1] == '0' && computationBits[2] == '1' && computationBits[3] == '0' && computationBits[4] == '1' && computationBits[5] == '0') {
			char computation[] = "0";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '1' && computationBits[1] == '1' && computationBits[2] == '1' && computationBits[3] == '1' && computationBits[4] == '1' && computationBits[5] == '1') {
			char computation[] = "1";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '1' && computationBits[1] == '1' && computationBits[2] == '1' && computationBits[3] == '0' && computationBits[4] == '1' && computationBits[5] == '0') {
			char computation[] = "-1";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '0' && computationBits[1] == '0' && computationBits[2] == '1' && computationBits[3] == '1' && computationBits[4] == '0' && computationBits[5] == '0') {
			char computation[] = "D";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '1' && computationBits[1] == '1' && computationBits[2] == '0' && computationBits[3] == '0' && computationBits[4] == '0' && computationBits[5] == '0') {
			char computation[] = "A";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '0' && computationBits[1] == '0' && computationBits[2] == '1' && computationBits[3] == '1' && computationBits[4] == '0' && computationBits[5] == '1') {
			char computation[] = "!D";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '1' && computationBits[1] == '1' && computationBits[2] == '0' && computationBits[3] == '0' && computationBits[4] == '0' && computationBits[5] == '1') {
			char computation[] = "!A";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '0' && computationBits[1] == '0' && computationBits[2] == '1' && computationBits[3] == '1' && computationBits[4] == '1' && computationBits[5] == '1') {
			char computation[] = "-D";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '1' && computationBits[1] == '1' && computationBits[2] == '0' && computationBits[3] == '0' && computationBits[4] == '1' && computationBits[5] == '1') {
			char computation[] = "-A";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '0' && computationBits[1] == '1' && computationBits[2] == '1' && computationBits[3] == '1' && computationBits[4] == '1' && computationBits[5] == '1') {
			char computation[] = "D+1";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '1' && computationBits[1] == '1' && computationBits[2] == '0' && computationBits[3] == '1' && computationBits[4] == '1' && computationBits[5] == '1') {
			char computation[] = "A+1";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '0' && computationBits[1] == '0' && computationBits[2] == '1' && computationBits[3] == '1' && computationBits[4] == '1' && computationBits[5] == '0') {
			char computation[] = "D-1";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '1' && computationBits[1] == '1' && computationBits[2] == '0' && computationBits[3] == '0' && computationBits[4] == '1' && computationBits[5] == '0') {
			char computation[] = "A-1";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '0' && computationBits[1] == '0' && computationBits[2] == '0' && computationBits[3] == '0' && computationBits[4] == '1' && computationBits[5] == '0') {
			char computation[] = "D+A";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '0' && computationBits[1] == '1' && computationBits[2] == '0' && computationBits[3] == '0' && computationBits[4] == '1' && computationBits[5] == '1') {
			char computation[] = "D-A";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '0' && computationBits[1] == '0' && computationBits[2] == '0' && computationBits[3] == '1' && computationBits[4] == '1' && computationBits[5] == '1') {
			char computation[] = "A-D";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '0' && computationBits[1] == '1' && computationBits[2] == '0' && computationBits[3] == '1' && computationBits[4] == '0' && computationBits[5] == '1') {
			char computation[] = "D|A";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else {
			char computation[] = "";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
	}
	else {
		if (computationBits[0] == '1' && computationBits[1] == '1' && computationBits[2] == '0' && computationBits[3] == '0' && computationBits[4] == '0' && computationBits[5] == '0') {
			char computation[] = "M";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '1' && computationBits[1] == '1' && computationBits[2] == '0' && computationBits[3] == '0' && computationBits[4] == '0' && computationBits[5] == '1') {
			char computation[] = "!M";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '1' && computationBits[1] == '1' && computationBits[2] == '0' && computationBits[3] == '0' && computationBits[4] == '1' && computationBits[5] == '1') {
			char computation[] = "-M";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '1' && computationBits[1] == '1' && computationBits[2] == '0' && computationBits[3] == '1' && computationBits[4] == '1' && computationBits[5] == '1') {
			char computation[] = "M+1";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '1' && computationBits[1] == '1' && computationBits[2] == '0' && computationBits[3] == '0' && computationBits[4] == '1' && computationBits[5] == '0') {
			char computation[] = "M-1";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '0' && computationBits[1] == '0' && computationBits[2] == '0' && computationBits[3] == '0' && computationBits[4] == '1' && computationBits[5] == '0') {
			char computation[] = "D+M";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '0' && computationBits[1] == '1' && computationBits[2] == '0' && computationBits[3] == '0' && computationBits[4] == '1' && computationBits[5] == '1') {
			char computation[] = "D-M";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '0' && computationBits[1] == '0' && computationBits[2] == '0' && computationBits[3] == '1' && computationBits[4] == '1' && computationBits[5] == '1') {
			char computation[] = "M-D";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '0' && computationBits[1] == '0' && computationBits[2] == '0' && computationBits[3] == '0' && computationBits[4] == '0' && computationBits[5] == '0') {
			char computation[] = "D&M";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else if (computationBits[0] == '0' && computationBits[1] == '1' && computationBits[2] == '0' && computationBits[3] == '1' && computationBits[4] == '0' && computationBits[5] == '1') {
			char computation[] = "D|A";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
		else {
			char computation[] = "";
			snprintf(computationString, sizeof(computationString), "%s", computation);
		}
	}
}


void create_c_instruction_string(const char* destString, const char* jumpString, const char* compString, char* fullString) {
	// Create full string by concatenating the destination, jump, and computation strings
	size_t index = 0;
	for (size_t i = 0; i < strlen(destString); i++) {
		fullString[index] = destString[i];
		index++;
	}
	for (size_t i = 0; i < strlen(compString); i++) {
		fullString[index] = compString[i];
		index++;
	}
	for (size_t i = 0; i < strlen(jumpString); i++) {
		fullString[index] = jumpString[i];
		index++;
	}
}


bool check_endianess(FILE* hmcFile) {
	// Create counters and increment each time the first 3 bits are set for big endian
	// Or increment each time the bits [8-10] are set for little endian
	bool littleEndian = false;
	short bigEndianCount = 0;
	short littleEndianCount = 0;
	unsigned char line[BINARY_LINE_SIZE] = { '\0' };
	unsigned char bytesRead = { '\0' };
	int integerToConvertOne = 0;
	int integerToConvertTwo = 0;
	char byteLineOne[BYTE_LENGTH] = { '\0' };
	char byteLineTwo[BYTE_LENGTH] = { '\0' };

	while (bytesRead = fread(line, sizeof(unsigned char), sizeof(line), hmcFile) > 0) {
		integerToConvertOne = line[0];
		integerToConvertTwo = line[1];
		convertDecimalToBinary(integerToConvertOne, byteLineOne);
		convertDecimalToBinary(integerToConvertTwo, byteLineTwo);
		
		if (byteLineOne[0] == '1') {
			bigEndianCount++;
		}
		else if (byteLineTwo[0] == '1') {
			littleEndianCount++;
		}
	}
	if (bigEndianCount < littleEndianCount) {
		littleEndian = true;
	}
	return littleEndian;
}


char* get_file_from_user(char* file) {
	// Prompt for file name and remove he newline character
	printf("Enter the file name: ");
	fgets(file, MAX_FILE_NAME, stdin);
	removeNewline(file);
	return file;
}


void removeNewline(char* array) {
	//Checking if the last index of the string length is newline, and changing it to null terminator
	if (array[strlen(array) - 1] == '\n') {
		array[strlen(array) - 1] = '\0';
	}
}


void convertDecimalToBinary(const int decimalToConvert, char* binaryLine) {
	clearCharArray(binaryLine);
	int decimal = decimalToConvert;
	// Set all values to 0
	for (size_t i = 0; i < sizeof(binaryLine); i++) {
		binaryLine[i] = '0';
	}
	binaryLine[sizeof(binaryLine)] = '\0';

	// Convert decimal to binary
	int index = sizeof(binaryLine) - 1;
	while (decimal > 0) {
		if (decimal % 2 != 0) {
			binaryLine[index] = '1';
		}
		decimal = decimal / 2;
		index--;
	}
}


void createTempFile(FILE* binaryFilePtr, const char* convertedFileName) {
	rewind(binaryFilePtr);
	unsigned char line[BINARY_LINE_SIZE] = { '\0' };
	unsigned char bytesRead = { '\0' };
	char binaryLine[BINARY_LINE_LENGTH] = { '\0' };
	int integerToConvertOne = 0;
	int integerToConvertTwo = 0;
	char byteLineOne[BYTE_LENGTH] = { '\0' };
	char byteLineTwo[BYTE_LENGTH] = { '\0' };
	FILE* tempFile = fopen(convertedFileName, "w");

	while (bytesRead = fread(line, sizeof(unsigned char), sizeof(line), binaryFilePtr) > 0) {
		clearCharArray(binaryLine);
		clearCharArray(byteLineOne);
		clearCharArray(byteLineTwo);

		integerToConvertOne = line[0];
		integerToConvertTwo = line[1];
		convertDecimalToBinary(integerToConvertOne, byteLineOne);
		convertDecimalToBinary(integerToConvertTwo, byteLineTwo);
		
		for (size_t i = 0; i < strlen(byteLineOne); i++) {
			binaryLine[i] = byteLineOne[i];
			binaryLine[i + sizeof(byteLineTwo) - 1] = byteLineTwo[i];
		}
		binaryLine[BINARY_LINE_LENGTH - 2] = '\n';
		binaryLine[BINARY_LINE_LENGTH - 1] = '\0';
		fprintf(tempFile, binaryLine);
	}
	fclose(tempFile);
}


void convertLittleEndianToBigEndian(const char* convertedFileName) {
	FILE* fileNeedsBytesSwitched = fopen(convertedFileName, "r");
	FILE* fileConvertedToBigEndian = fopen("convertedToBigEndianDeleteMe.hack", "w");
	char tempByte[9] = { '\0' };
	char line[BINARY_LINE_LENGTH] = { '\0' };
	
	while (fgets(line, sizeof(line), fileNeedsBytesSwitched)) {
		clearCharArray(tempByte);

		for (size_t i = 0; i < sizeof(tempByte) - 1; i++) {
			tempByte[i] = line[i];
		}
		for (size_t i = 0; i < sizeof(tempByte) - 1; i++) {
			line[i] = line[i + 8];
		}
		for (size_t i = 0; i < sizeof(tempByte) - 1; i++) {
			line[i + 8] = tempByte[i];
		}
		fprintf(fileConvertedToBigEndian, line);
	}
	fclose(fileNeedsBytesSwitched);
	fclose(fileConvertedToBigEndian);
}


void clearCharArray(char* array) {
	for (int i = sizeof(array); i >= 0; i--) {
		array[i] = '\0';
	}
}