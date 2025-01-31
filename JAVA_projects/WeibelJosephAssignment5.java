import java.io.FileNotFoundException;
import java.io.File;
import java.util.ArrayList;
import java.util.Scanner;

public class WeibelJosephAssignment5 {

	public static void main(String[] args) {
		//Create integer and string stack that invokes the constructor and creates an empty array list of that type
		GenericStack<Integer> integerStack = new GenericStack<Integer>();
		GenericStack<String> stringStack = new GenericStack<String>();
		//Create a File object that reads the specified text file
		File numbersSpringFile = new File("numbersSpring.txt");
		File stringsSpringFile = new File("stringsSpring.txt");

		try {
			//attempt to create two scanner objects, one for ints and one for strings
			Scanner fileScannerInt = new Scanner(numbersSpringFile);
			Scanner fileScannerString = new Scanner(stringsSpringFile);
			
			//iterate over the integer file until there is no more input
			while(fileScannerInt.hasNextLine()) {
				//Add the first line to a temp variable that only has scope in the while loop
				String line = fileScannerInt.nextLine();
				//change the data type to int
				int lineNum = Integer.parseInt(line);
				//add the value to the int stack
				integerStack.push(lineNum);
			}
			//iterate over the string file until there are no more values to iterate over
			while(fileScannerString.hasNextLine()) {
				// read contents and add the line to a temp variable with scope inside the while loop
				String line = fileScannerString.nextLine();
				//add the value to the string stack
				stringStack.push(line);
			}
			
			//Close both scanner objects to prevent data leaks
			fileScannerInt.close();
			fileScannerString.close();
		} catch(FileNotFoundException e) {
			//Exception handling in case the file is not found or scanner object cannot be created
			e.printStackTrace();
		}
		
		//Print statements for reading data from the file
		System.out.println("Values read from file and pushed onto number stack:");
		System.out.println("----------------------------------------------------");
		//Calling printStack which expects the GenericStack object as an argument of type E
		printStack(integerStack);
		System.out.println("");
		
		//Calling sortStack which expects the GenericStack object as an argument of type E to sort in numerical order
		sortStack(integerStack);
		
		System.out.println("Number Stack sorted - smallest to highest:");
		System.out.println("----------------------------------------------------");
		//Calling printStack which expects the GenericStack object as an argument of type E
		printStack(integerStack);
		System.out.println("");
		
		//Create scanner object that takes input from the keyboard aka user for both int values to replace and search for
		Scanner scanner = new Scanner(System.in);
		System.out.print("Enter value to replace on integer stack: ");
		int valueToBeReplacedInt = scanner.nextInt();
		System.out.print("Enter the replacement value: ");
		int replacementValueInt = scanner.nextInt();
		System.out.println("");
		
		System.out.printf("Number Stack - replaced %d with %d:\n", valueToBeReplacedInt, replacementValueInt);
		System.out.println("------------------------------------");
		//calling searchAndReplace which expects the genericStack as an argument and the two integer values to by found and replaced
		searchAndReplace(integerStack, valueToBeReplacedInt, replacementValueInt);
		//Calling printStack which expects the GenericStack object as an argument of type E
		printStack(integerStack);
		System.out.println("");
		
		System.out.println("read from file and pushed onto string Stack:");
		System.out.println("-----------------------------------------------------");
		//Calling printStack which expects the GenericStack object as an argument of type E
		printStack(stringStack);
		System.out.println("");
		
		System.out.println("Stack sorted - alphabetical order:");
		System.out.println("----------------------------------------------");
		//calling sortStack to sort the values in alphabetical order
		sortStack(stringStack);
		//Calling printStack which expects the GenericStack object as an argument of type E
		printStack(stringStack);
		System.out.println("");
		
		System.out.print("Enter value to replace on string stack: ");
		String valueToBeReplacedString = scanner.next();
		System.out.print("Enter the replacement value: ");
		String replacementValueString = scanner.next();
		System.out.println("");
		//Close scanner object to prevent memory leak
		scanner.close();
		
		System.out.printf("String Stack - replaced %s with %s\n", valueToBeReplacedString, replacementValueString);
		System.out.println("----------------------------------------------------------------");
		//calling searchAndReplace which expects the genericStack as an argument and the two string values to by found and replaced
		searchAndReplace(stringStack, valueToBeReplacedString, replacementValueString);
		//Calling printStack which expects the GenericStack object as an argument of type E
		printStack(stringStack);
	}
	
	
	public static <E extends Comparable<E>> void sortStack(GenericStack<E> stack) {
	    GenericStack<E> tempStack = new GenericStack<>();
	    while (!stack.isEmpty()) {
	        E smallest = removeSmallestElement(stack);
	        tempStack.push(smallest);
	    }
	    
	    while (!tempStack.isEmpty()) {
	        stack.push(tempStack.pop());
	    }
	}
	public static <E extends Comparable<E>> E removeSmallestElement(GenericStack<E> stack) {
		GenericStack<E> tempStack = new GenericStack<>();
		E smallest = stack.pop();
		
		while(!stack.isEmpty()) {
			E current = stack.pop();
			if (current.compareTo(smallest) < 0){
				tempStack.push(smallest);
				smallest = current;
			}
			else {
				tempStack.push(current);
			}
		}
		
		while(!tempStack.isEmpty()) {
			E item = tempStack.pop();
			if(!item.equals(smallest)) {
				stack.push(item);
			}
		}
		
		return smallest;
		
	}
	 public static <E extends Comparable<E>> void printStack(GenericStack<E> stack) {
		 GenericStack<E> tempStack = new GenericStack<>();
		 
	     while (!stack.isEmpty()) {
	         E item = stack.pop();
	         System.out.println(item);
	         tempStack.push(item);
	     }

	     while (!tempStack.isEmpty()) {
	         stack.push(tempStack.pop());
	     }	     
	 }
	 public static <E> boolean searchAndReplace(GenericStack<E> stack, E valueToReplace, E replacementValue) {
	        GenericStack<E> tempStack = new GenericStack<>();
	        boolean replaced = false;

	        while (!stack.isEmpty()) {
	            E currentItem = stack.pop();

	            if (currentItem.equals(valueToReplace)) {
	                tempStack.push(replacementValue);
	                replaced = true;
	            } else {
	                tempStack.push(currentItem);
	            }
	        }

	        while (!tempStack.isEmpty()) {
	            stack.push(tempStack.pop());
	        }

	        return replaced;
	    }
}

class GenericStack<E>{
	private ArrayList<E> list;
	
	public GenericStack() {
		list = new ArrayList<E>();
	}
	public int getSize(){
		return list.size();
	}
	public boolean isEmpty() {
		return list.isEmpty();
	}
	public E peek() {
		return list.get(getSize()-1);
	}
	public void push(E value) {
		list.add(value);
	}
	public E pop() {
		return list.remove(getSize() - 1);
	}

}