/*
Name: Joseph Weibel
Class: 2024Sp CS 1450 003
Section: 1
Due: Apr 1, 2024
Description: Assignment #8
This program will read from a file and get the secret messages from two separate files using array lists.
Create classes with decoder methods to unscramble the cipher method. These methods will require the iterator to be passed
to the method.
*/

import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;
import java.io.File;
import java.io.FileNotFoundException;

public class WeibelJosephAssignment8 {

	public static void main(String[] args) {
		ArrayList<Character> secretMessage1 = new ArrayList<>();
		ArrayList<Character> secretMessageKeys1 = new ArrayList<>();
		Queue<Character> messageQueue = new LinkedList<>();
		Queue<Character> messageQueueKeys = new LinkedList<>();
		int rows = 0;
		int columns = 0;
		int startingRow = 0;
		int startingColumn = 0;
		String originalMessage1 = "";
		String originalMessageQueue = "";
		
		try {
			Scanner messageScanner = new Scanner(new File("listMessage.txt"));
			Scanner messageKeyScanner = new Scanner(new File("listKey.txt"));
			
			while(messageScanner.hasNextLine()) {
				String line = messageScanner.nextLine();
				originalMessage1 = line;
				
				for(char letter : line.toCharArray()) {
					if(Character.isLetter(letter) || letter == '-' || letter == '!') {
						secretMessage1.add(letter);
					}
				}
			}
			messageScanner.close();
			
			String keysForMessage = messageKeyScanner.nextLine();
			for (char letter : keysForMessage.toCharArray()) {
			    secretMessageKeys1.add(letter);
			}
			
			String[] sizeArray = messageKeyScanner.nextLine().split(" ");
			rows = Integer.parseInt(sizeArray[0]);
			columns = Integer.parseInt(sizeArray[1]);
			
			String[] startingArray = messageKeyScanner.nextLine().split(" ");
			startingRow = Integer.parseInt(startingArray[0]);
			startingColumn = Integer.parseInt(startingArray[1]);
			messageKeyScanner.close();
			
		} catch (FileNotFoundException e) {
			System.out.println("Error finding file");
		}
		
		Iterator<Character> msgIterator = secretMessage1.iterator();
		Iterator<Character> keyIterator = secretMessageKeys1.iterator();
		
		Decoder decoder1 = new Decoder(rows, columns, startingRow, startingColumn);
		String message = decoder1.unscramble(msgIterator, keyIterator);
		
		System.out.println("For the 1st set of files (listMessage.txt and listKey.txt):\n");
		System.out.printf("The original message is: %s\n", originalMessage1);
		System.out.printf("The secret message is: %s\n", message);
		
		
		
		try {
			Scanner messageScannerQueue = new Scanner(new File("queueMessage.txt"));
			Scanner messageKeyScannerQueue = new Scanner(new File("queueKey.txt"));
			
			while(messageScannerQueue.hasNextLine()) {
				String line = messageScannerQueue.nextLine();
				originalMessageQueue = line;
				
				for(char letter : line.toCharArray()) {
					if(Character.isLetter(letter) || letter == '-' || letter == '!') {
						messageQueue.add(letter);
					}
				}
			}
			messageScannerQueue.close();
			
			String keysForMessage = messageKeyScannerQueue.nextLine();
			for (char letter : keysForMessage.toCharArray()) {
				messageQueueKeys.add(letter);
			}
			
			String[] sizeArray = messageKeyScannerQueue.nextLine().split(" ");
			rows = Integer.parseInt(sizeArray[0]);
			columns = Integer.parseInt(sizeArray[1]);
			
			String[] startingArray = messageKeyScannerQueue.nextLine().split(" ");
			startingRow = Integer.parseInt(startingArray[0]);
			startingColumn = Integer.parseInt(startingArray[1]);
			messageKeyScannerQueue.close();
			
		} catch (FileNotFoundException e) {
			System.out.println("Error finding file");
		}
		
		
		Iterator<Character> msgIteratorQueue = messageQueue.iterator();
		Iterator<Character> keyIteratorQueue = messageQueueKeys.iterator();
		
		Decoder decoderQueue = new Decoder(rows, columns, startingRow, startingColumn);
		String queueMessage = decoderQueue.unscramble(msgIteratorQueue, keyIteratorQueue);
		
		System.out.println("\nFor the 2nd set of files (queueMessage.txt and queueKey.txt):\n");
		System.out.printf("The original message is: %s\n", originalMessageQueue);
		System.out.printf("The secret message is: %s", queueMessage);
	}

}


class Decoder{
	private char[][] messageArray;
	private int startingRow;
	private int startingCol;
	private Stack stack;
	
	public Decoder(int numRows, int numCols, int startingRow, int startingCol) {
		this.messageArray = new char[numRows][numCols];
		this.startingRow = startingRow;
		this.startingCol = startingCol;
		this.stack = new Stack();
	}
	
	public String unscramble(Iterator<Character> msgIterator, Iterator<Character>keyIterator) {
		StringBuilder message = new StringBuilder();
		
		for(int row = this.messageArray.length - 1; row >= 0 ; row--) {
			for(int column = 0; column < this.messageArray[row].length; column++) {
				if(msgIterator.hasNext()) {
					messageArray[row][column] = msgIterator.next();
				}
			}
		}
		stack.push(messageArray[startingRow][startingCol]);		
		
		while(keyIterator.hasNext()) {
			char key = keyIterator.next();
			if(key == 'u') {
				startingRow--;
			}
			else if(key == 'b') {
				startingCol--;
			}
			else if(key == 'f') {
				startingCol++;
			}
			else if(key == 'd') {
				startingRow++;
			}

			stack.push(messageArray[startingRow][startingCol]);
		}
		
		while(!stack.isEmpty()) {
			message.append(stack.pop());
		}
		return message.toString();
	}
}


class Stack{
	private ArrayList<Character> list;
	
	public Stack() {
		list = new ArrayList<>();
	}
	public boolean isEmpty() {
		return list.isEmpty();
	}
	public int getSize() {
		return list.size();
	}
	public void push(Character value) {
		list.add(value);
	}
	public Character pop() {
		if (!isEmpty()) {
			return list.remove(list.size()-1);
		}
		return null;
	}
}