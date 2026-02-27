//Import statements for required libraries for the program
import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.Random;

//Beginning of the assignment class. This class will create a file and input 25 random numbers into it and then pull the numbers out of the file
//and place the numbers in a new array and find the two largest numbers without including duplicates. Then the program will sort the array into
//descending order.
public class WeibelJosephAssignment1 {
	
	//Beginning of the main method for the class
    public static void main(String[] args) throws IOException {
    	//Declare all variables and create objects for the program
        File fileName = new File("assignment1.txt");
        FileWriter writerObject;
        int randomNumberArray[] = new int[25];
        int secondRandomNumberArray[] = new int[25];
        Random randomNumberObject = new Random();
        int largest = 0;
        int secondLargest = 0;
        int temp;
        
        //Generate 25 random numbers 1-100 and place them in an array
        System.out.println("Generating random values and writing to a file");
        for (int i = 0; i < 25; i++) {
            randomNumberArray[i] = randomNumberObject.nextInt(100) + 1;
        }

        try {
        	//Create a file writer object and write the array values to the file
        	//While writing the values to the file print the values to the console
            writerObject = new FileWriter(fileName);
            for (int i = 0; i < randomNumberArray.length; i++) {
                writerObject.write(randomNumberArray[i] + "\n");
                System.out.printf("Writing to file: %d\n", randomNumberArray[i]);
            }
            //Close the file writer object
            writerObject.close();
            
            //Create file reader object to be used to pull values from .txt file
            BufferedReader reader = new BufferedReader(new FileReader(fileName));

            String line;
            int i = 0;
            System.out.println("\nReading values from file and placing into an array");
            
            //Read all values from the file and place each value in a new array
            //Print the values of the new array after they are placed from the file
            while ((line = reader.readLine()) != null && i < secondRandomNumberArray.length) {
                secondRandomNumberArray[i] = Integer.parseInt(line);
                System.out.printf("Value in array: %d\n", secondRandomNumberArray[i]);
                i++;
            }
            //Close the reader object
            reader.close();

        } catch (IOException e) {
            e.printStackTrace();
        }
        
        //Pull the two largest values from the new array without recognising duplicate values
        System.out.println("\nFinding the largest two values in the array");
        for (int i = 0 ; i < 25; i++) {
        	if (secondRandomNumberArray[i] > secondLargest && secondRandomNumberArray[i] != largest) {
        		secondLargest = secondRandomNumberArray[i];
        		if (secondLargest > largest) {
        			temp = largest;
        			largest = secondLargest;
        			secondLargest = temp;
        		}
        	}
        }
        
        //Print statements for the two largest values
        System.out.printf("1st Largest value: %d\n", largest);
        System.out.printf("2nd Largest value: %d\n", secondLargest);
        
        //Use the Arrays.sort() method to sort the array into ascending order
        System.out.println("\nSorting the values in the array into descending order (largest to smallest)");
        Arrays.sort(secondRandomNumberArray);
        
        //Manually sort the array from ascending order into descending order
        int j = secondRandomNumberArray.length-1;
        for(int i = 0; i < secondRandomNumberArray.length/2; i++) {
        	temp = secondRandomNumberArray[i];
        	secondRandomNumberArray[i] = secondRandomNumberArray[j];
        	secondRandomNumberArray[j] = temp;
        	j--;
        }
        
        //Print the values from the newly sorted array in descending order
        for(int i = 0; i < 25; i++) {
        	System.out.printf("Numbers[%d] = %d\n", i, secondRandomNumberArray[i]);
        }
    }
}
