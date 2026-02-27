/*
Name: Joseph Weibel
Class: 2024Sp CS 1450 003
Section: 1
Due: Apr 8, 2024
Description: Assignment #9
This program will read from a file a route that the parrots are taking from their tour.
This program will read the input from the file as destinations and store them in a singly linked list.
This program will then print the destinations.
After this program prints the destinations there are replacement destinations that will be swapped out in the list.
Then the list will be printed again.
*/

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class WeibelJosephAssignment9 {

	public static void main(String[] args) {
		//Create instance and invoke constructor
		TourLinkedList tourLinkedList = new TourLinkedList();
		
		try {
			//Creating a scanner object, expects a file object with path to file, will return a scanner object to read the file
			Scanner concertTourScanner = new Scanner(new File("concertTour.txt"));
			
			while(concertTourScanner.hasNextLine()) {
				String line = concertTourScanner.nextLine();
				//line is read from the file and split into 4 indexes with a space as the delimeter and will return an array
				String lineArray[] = line.split(" ", 4);
				//parseint expects a string as an argument and will return that string as an integer
				int fileStop = Integer.parseInt(lineArray[0]);
				String fileType = lineArray[1];
				String fileName = lineArray[2];
				String fileActivity = lineArray[3];
				
				//Declaring and initializing a locale, this expects the values from the file as arguments.
				//This will take in an int as a stop, String as type, String as name, and String as activity
				// This will invoke the constructor and create the locale
				Locale locale = new Locale(fileStop, fileType, fileName, fileActivity);
				//This method addLocale expects a locale as an argument and will add it to the linked list and wont return anything
				tourLinkedList.addLocale(locale);
			}
			//Close scanner object
			concertTourScanner.close();
		} catch (FileNotFoundException e) {
			System.out.println("Error finding initial tour file");
		}
		
		
		
		System.out.println("Unsorted Concert Tour Route");
		System.out.println("Locale\t\t\tType\t\t\tActivity");
		System.out.println("----------------------------------------------------------------------------------");
		//Does not expect arguments or return anything, will print the entire linked list as it appears
		tourLinkedList.printList();
		System.out.println();
		
		System.out.println("Sorted Concert Tour Route");
		System.out.println("Locale\t\t\tType\t\t\tActivity");
		System.out.println("----------------------------------------------------------------------------------");
		//Does not require any arguments and does not return anything. This method wont print anything and will only sort 
		//Using the bubble sort method
		tourLinkedList.bubbleSort();
		//Does not expect arguments or return anything, will print the entire linked list as it appears
		tourLinkedList.printList();
		
		
		try {
			//Creating a scanner object, expects a file object with path to file, will return a scanner object to read the file
			Scanner tourReplacementScanner = new Scanner(new File("concertTourReplace.txt"));
			while (tourReplacementScanner.hasNextLine()) {
				String line = tourReplacementScanner.nextLine();
				//line is read from the file and split into 4 indexes with a space as the delimeter and will return an array
				String lineArray[] = line.split(" ", 4);
				//parseint expects a string as an argument and will return that string as an integer
				int fileStop = Integer.parseInt(lineArray[0]);
				String fileType = lineArray[1];
				String fileName = lineArray[2];
				String fileActivity = lineArray[3];
				
				//Declaring and initializing a locale, this expects the values from the file as arguments.
				//This will take in an int as a stop, String as type, String as name, and String as activity
				// This will invoke the constructor and create the locale
				Locale replacementLocale = new Locale(fileStop, fileType, fileName, fileActivity);
				//This method addLocale expects a locale as an argument and will add it to the linked list and wont return anything
				tourLinkedList.replaceLocale(replacementLocale);
				
			}
			tourReplacementScanner.close();
		} catch (FileNotFoundException e) {
			System.out.println("Error finding tour replacement file");
		}
		
		System.out.println("\nUpdated Concert Tour Route - Replaced Certain Locales");
		System.out.println("Locale\t\t\tType\t\t\tActivity");
		System.out.println("----------------------------------------------------------------------------------");
		//Does not expect arguments or return anything, will print the entire linked list as it appears
		tourLinkedList.printList();
	}

}

//This class represents a locale object the will be used to add to the linked list. Upon creation will take in the stop
//type, name, and activity as arguments to invoke the constructor
class Locale implements Comparable<Locale>{
	private int stop;
	private String type;
	private String name;
	private String activity;
	
	//Constructor for Locale
	public Locale(int stop, String type, String name, String activity) {
		this.stop = stop;
		this.type = type;
		this.name = name;
		this.activity = activity;
	}
	//Used to get the stop of an object, returns an int
	public int getStop() {
		return this.stop;
	}
	//Used to set the stop, expects an int as an argument to replace the stop
	public void setStop(int stop) {
		this.stop = stop;
	}
	//Used to get the type, takes no arguments but returns a String to represent the type
	public String getType() {
		return this.type;
	}
	//Takes a String representing the type as an argument and will not reutrn anything. Sets the type to the argument for the object
	public void setType(String type) {
		this.type = type;
	}
	//Returns a String representing the name, takes no arguments
	public String getName() {
		return this.name;
	}
	//Expects a String representing a name as an argument and will set the name to the argument, returns nothing
	public void setName(String name) {
		this.name = name;
	}
	//Takes no arguments, returns a String representing the acitivty
	public String getActivity() {
		return this.activity;
	}
	//Takes a String as an argument for the activity, sats the activity, returns nothing
	public void setActivity(String activity) {
		this.activity = activity;
	}
	//Prints the object in a formatted string
	public String print() {
		return String.format("%d %-23s %-23s %s",this.stop, this.name, this.type, this.activity);
	}
	//Overrides the compareTo of the class that was imported and is used to compare on object to another and return the result when called
	@Override
	public int compareTo(Locale other) {
		return Integer.compare(this.stop, other.stop);
	}
}

//Used to store all locales in a linked list
class TourLinkedList{
	private Node head;
	private Node tail;
	private int size;
	
	//Constructor takes no arguments and initializes head and tail to null and size to 0 for incrementing
	public TourLinkedList() {
		this.head = null;
		this.tail = null;
		this.size = 0;
	}
	//Used to add locale, takes a locale object as an argument and creates a temp node object, then checks if head is null and sets head and tail to the node
	//If head is not null that means there are other locales and will add the node to tail.next and increment size no matter what
	public void addLocale(Locale locale) {
		Node node = new Node(locale);
		
		if (head == null) {
			head = node;
			tail = node;
		}
		else {
			tail.next = node;
			tail = node;
		}
		this.size++;
	}
	//Expects a Locale object as an argument and returns nothing. Will iterate through the list of nodes and check if the stop is the same and replace that node
	//If the stop is not the same it will movce the current node to the next node. This method returns nothing
	public void replaceLocale(Locale replacementLocale) {
		Node currentNode = head;
		for(int i = 0; i < size; i++) {
			if (currentNode.locale.getStop() == replacementLocale.getStop()) {
				currentNode.locale = replacementLocale;
			}
			else {
				currentNode = currentNode.next;
			}
		}
	}
	//Uses two embedded for loops to increment through the nodes, inside the outer for loop it will set the current next nodes
	//the inner loop will compare stops and swap nodes if a condition is met, whether the condition is met or not will mode on to the next nodes for the comparison
	public void bubbleSort() {
		for(int i = 0; i < size - 1; i++) {
			Node currentNode = head;
			Node nextNode = currentNode.next;
			for(int j = 0; j < size - 1 - i; j++) {
				if(currentNode.locale.getStop() > nextNode.locale.getStop()) {
					//Expects two Node data types as arguments, will not return anything, will only swap the positon of the nodes in the list.
					swapNodeData(currentNode, nextNode);
				}
				currentNode = nextNode;
				nextNode = nextNode.next;
			}
		}
	}
	//Takes two node objects as arguments and swaps their location in the list. Does not return anything
	public void swapNodeData(Node node1, Node node2) {
		Locale temp = node1.locale;
		node1.locale = node2.locale;
		node2.locale = temp;
	}
	//Takes no arguments and prints the whole list, does not return anything.
	public void printList() {
		Node currentNode = head;
		while(currentNode != null) {
			System.out.println(currentNode.locale.print());
			currentNode = currentNode.next;
		}
	}
	
	//Class only accessible inside TourLinkedList and is used to create nodes, the constructor takes locale as an argument for the constructor
	private class Node{
		private Locale locale;
		private Node next;
		//Constructor that creates a locale and sets the next Node to null
		public Node(Locale locale) {
			this.locale = locale;
			this.next = null;
		}
	}
}