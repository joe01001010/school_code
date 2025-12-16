#!/usr/bin/env python3
import sys
import numpy as np


# Hardcoding the encoding matrix and using it to create the decoding matrix
# This creates the rows which are used for dimensions for padding the matrices in the future
ENCODING_MATRIX = np.array([
        [ 1, -1, -1, 1],
        [ 2, -3, -5, 4],
        [-2, -1, -2, 2],
        [ 3, -3, -1, 2]
    ])
DECODING_MATRIX = np.linalg.inv(ENCODING_MATRIX)
ROWS = ENCODING_MATRIX.shape[0]


def main():
    """
    This function takes no arguments and doesnt return anything
    This function will read contents from a file and print the original message to the screen
    This function will pass the space separated text to the encrypt_message function the encrypt it
    The function will then write the encrypted message to a new file and print it to the screen
    This function will then read that message from a file and then decrypt that message
    """
    file_contents = read_file("input-A21.txt")
    print(f"Original Plaintext Message:\n{file_contents}")
    encrypted_matrix = encrypt_message(file_contents)
    write_file("encrypted-A21.txt", ' '.join(map(str, encrypted_matrix.flatten())))
    file_contents = read_file("encrypted-A21.txt")
    decrypted_matrix = decrypt_message(file_contents)
    sys.exit(0)


def decrypt_message(encrypted_string):
    """
    This function will take an encrypted list of values as an argument
    Converts the encrypted string to a matrix
    Decrypts the message using the decoding matrix
    This function will convert the decrypted matrix to a readable string
    This function will print the decrypted matrix
    Returns the decrypted message as a string
    """
    encrypted_values = [int(value) for value in encrypted_string.split()]
    encrypted_matrix = np.array(encrypted_values).reshape(ROWS, -1)
    decrypted_matrix = np.dot(DECODING_MATRIX, encrypted_matrix)
    decrypted_unicode_values = np.rint(decrypted_matrix).astype(int).flatten()
    decrypted_message = ''.join(chr(value) for value in decrypted_unicode_values if 0 < value < 0x110000)

    print("\nDecrypted Message:\n", decrypted_message)
    return decrypted_message


def encrypt_message(message):
    """
    This function will take a plaintext message as a string as an argument
    Encrypts a message using the encoding matrix
    This function will print the plaintext matrix and the encrypted matrix
    Returns the encrypted message as a matrix
    """
    unicode_values = [ord(char) for char in message]
    
    remainder = len(unicode_values) % ROWS
    if remainder != 0:
        unicode_values.extend([0] * (ROWS - remainder))

    plaintext_matrix = np.array(unicode_values).reshape(ROWS, -1)
    encrypted_matrix = np.rint(np.dot(ENCODING_MATRIX, plaintext_matrix)).astype(int)

    print(f"Plaintext Matrix:\n{plaintext_matrix}")
    print(f"Encrypted Matrix:\n{encrypted_matrix}")
    return encrypted_matrix


def read_file(file_path):
    """
    Reads the contents of a file and returns it as a string.
    If the file is not found it will prompt the user for contents to encrypt
    If no content is entered to encrypt the program will exit with return code 0
    """
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        content = input("Enter message to encrypt: ")
        if len(content) > 0:
            return content
        print("No message entered. Exiting.")
        sys.exit(0)


def write_file(file_path, content):
    """
    This function takes two arguments, a file path as a string
    The second argument is the content to write to the file as a string
    If the file is not found it will exit the program with a status code of 1
    """
    try:
        with open(file_path, "w") as file:
            file.write(content)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()