import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

public class WeibelJosephAssignment3 {

	public static void main(String[] args) {
		//Declare and initialize variables for reading a file
		String arraySizeString = "";
		int arraySizeInt = 0;
		
		try {
			//Create a BufferedReader object that reads the specified text file
			BufferedReader reader = new BufferedReader(new FileReader("athletes.txt"));
			arraySizeString = reader.readLine();
			reader.close();
		} catch(IOException e) {
			e.printStackTrace();
		}
		//With the return form the firest line in the file change the value to an integer and save in a variable for array size
		arraySizeInt = Integer.parseInt(arraySizeString.trim());
		Athlete[] athleteArray = new Athlete[arraySizeInt];
		
		try {
			//Create a file reader objext again to read the same file
			BufferedReader reader = new BufferedReader(new FileReader("athletes.txt"));
			reader.readLine();
			String line;
			int i = 0;
			
			//Iterate over the lines in the file until there are no more lines left to read
			while ((line = reader.readLine()) != null) {
				//Split the line read into different sections based off a delimiter of a space
				String[] sections = line.split(" ");
				String type = sections[0];
				double runSpeed = Double.parseDouble(sections[1]);
				double swimSpeed = Double.parseDouble(sections[2]);
				double bikeSpeed = Double.parseDouble(sections[3]);
				// Combine the last two sections to be one name
				String name = sections[4] + " " + sections[5];
				
				// Based off the first section that is stored in a variable we will compare that and create the appropriate object
				if (type.equals("t")) {
					athleteArray[i] = new Triathlete(name, runSpeed, swimSpeed, bikeSpeed, "Triathlete");
				}
				else if (type.equals("d")) {
					athleteArray[i] = new Duathlete(name, runSpeed, bikeSpeed, "Duathlete");
				}
				else if (type.equals("a")) {
					athleteArray[i] = new Aquathlete(name, runSpeed, swimSpeed, "Aquathlete");
				}
				else if (type.equals("m")) {
					athleteArray[i] = new Marathoner(name, runSpeed, "Marathoner");
				}
				else {
					System.out.println("No matching turtle types found for: " + type);
				}
				i++;
			}
			reader.close();
		} catch(IOException e) {
			e.printStackTrace();
		}
		//Pass the athleteArray as an argument to the find bikers method that will return an array list of athletes that ride bikes
		ArrayList<Athlete> bikersArrayList = findBikers(athleteArray);
		//Pass the athleteArray as an argument to the findDoNotSwim method that will return an ArrayList of athletes that do not swim
		ArrayList<Athlete> doNotSwimArrayList = findDoNotSwim(athleteArray);
		//Pass the athleteArray as an argument to the slowest runner method to find who the slowest runner is
		Athlete slowestRunner = findSlowestRunner(athleteArray);
		
		
		System.out.println("ATHLETES THAT BIKE!");
		System.out.println("----------------------");
		
		//Cycle through the array list and use a conditional to determine if the athlete child class will be triathlete or duathlete
		// This will allow us to ensure proper casting for the interfaces being called
		for(Athlete athlete : bikersArrayList) {
			if(athlete instanceof Triathlete) {
				System.out.println(athlete.getName() + " is a " + athlete.getType() + " and is an athlete that bikes at "  + ((Triathlete) athlete).bike());
				System.out.println(athlete.disciplines());
			}
			else if(athlete instanceof Duathlete) {
				System.out.println(athlete.getName() + " is a " + athlete.getType() + " and is an athlete that bikes at "  + ((Duathlete) athlete).bike());
				System.out.println(athlete.disciplines());
			}
			System.out.println();
		}
		
		//Cycle through the array list and print the appropriate statement for athletes that dont swim
		//This loop doesn't require a conditional as there is no casting required
		System.out.println("ATHLETES THAT DO NOT SWIM!");
		System.out.println("----------------------");
		for(Athlete athlete : doNotSwimArrayList) {
			System.out.println(athlete.getName() + " is a " + athlete.getType() + " and does not swim");
			System.out.println(athlete.disciplines());
			System.out.println();
		}
		
		//Print out the slowest runner. There needs to be a conditional check to ensure the correct type of athlete is being checked and casted 
		System.out.println("SLOWEST RUNNER!");
		System.out.println("----------------------");
		if(slowestRunner instanceof Triathlete) {
			System.out.println("Slowest runner is " + slowestRunner.getName() + " who is a " + slowestRunner.getType() + " with a running speed of " + ((Triathlete) slowestRunner).run());
		}
		else if(slowestRunner instanceof Duathlete) {
			System.out.println("Slowest runner is " + slowestRunner.getName() + " who is a " + slowestRunner.getType() + " with a running speed of " + ((Duathlete) slowestRunner).run());
		}
		else if(slowestRunner instanceof Aquathlete) {
			System.out.println("Slowest runner is " + slowestRunner.getName() + " who is a " + slowestRunner.getType() + " with a running speed of " + ((Aquathlete) slowestRunner).run());
		}
		else if(slowestRunner instanceof Marathoner) {
			System.out.println("Slowest runner is " + slowestRunner.getName() + " who is a " + slowestRunner.getType() + " with a running speed of " + ((Marathoner) slowestRunner).run());
		}
		
	}// End main method
	
	public static ArrayList<Athlete> findDoNotSwim(Athlete[] athletes){
		ArrayList<Athlete> doNotSwim = new ArrayList<>();
		for(int i = 0; i < athletes.length; i++) {
			if(athletes[i] instanceof Duathlete || athletes[i] instanceof Marathoner) {
				doNotSwim.add(athletes[i]);
			}
		}
		return doNotSwim;
		
	}
	public static ArrayList<Athlete> findBikers(Athlete [] athletes){
		ArrayList<Athlete> bikers = new ArrayList<>();
		for(int i = 0; i < athletes.length; i++) {
			if(athletes[i] instanceof Duathlete || athletes[i] instanceof Triathlete) {
				bikers.add(athletes[i]);
			}
		}
		return bikers;		
	}	
	
	public static Athlete findSlowestRunner(Athlete[] athletes) {
		double slowestSpeed = 100.00;
		Athlete slowestRunner = null;
		
		for(int i = 0; i < athletes.length; i++) {
			if(athletes[i] instanceof Triathlete) {
				if(((Triathlete) athletes[i]).run() < slowestSpeed) {
					slowestSpeed = ((Triathlete) athletes[i]).run();
					slowestRunner = athletes[i];
				}
			}
			else if(athletes[i] instanceof Duathlete) {
				if(((Duathlete) athletes[i]).run() < slowestSpeed) {
					slowestSpeed = ((Duathlete) athletes[i]).run();
					slowestRunner = athletes[i];
				}
			}
			else if(athletes[i] instanceof Aquathlete) {
				if(((Aquathlete) athletes[i]).run() < slowestSpeed) {
					slowestSpeed = ((Aquathlete) athletes[i]).run();
					slowestRunner = athletes[i];
				}
			}
			else if(athletes[i] instanceof Marathoner) {
				if(((Marathoner) athletes[i]).run() < slowestSpeed) {
					slowestSpeed = ((Marathoner) athletes[i]).run();
					slowestRunner = athletes[i];
				}
			}
		}
		return slowestRunner;
	}
} //End main class

interface Runner{
	public double run();
}
interface Swimmer{
	public double Swim();
}
interface Biker{
	public double bike(); 
}


abstract class Athlete{
	protected String name;
	protected String type;
	
	public String getName() {
		return this.name;
	}
	public void setName(String name) {
		this.name = name;
	}
	public String getType() {
		return this.type;
	}
	public void setType(String type) {
		this.type = type;
	}
	
	public abstract String disciplines();
}//End athlete superclass

class Triathlete extends Athlete implements Runner, Swimmer, Biker{
	private double swimSpeed;
	private double runSpeed;
	private double bikeSpeed;
	
	Triathlete(String name, double runSpeed, double swimSpeed, double bikeSpeed, String type){
		this.name = name;
		this.type = type;
		this.runSpeed = runSpeed;
		this.bikeSpeed = bikeSpeed;
		this.swimSpeed = swimSpeed;
	}

	@Override
	public String disciplines() {
		return "During the Ironman Triathlon, I swim 2.4 miles, bike 112 mils, then run 26.2 miles.";
	}

	@Override
	public double bike() {
		return this.bikeSpeed;
	}

	@Override
	public double Swim() {
		return this.swimSpeed;
	}

	@Override
	public double run() {
		return this.runSpeed;
	}
	
}// End triathlete class


class Duathlete extends Athlete implements Runner, Biker{
	
	private double runSpeed;
	private double bikeSpeed;
	
	Duathlete(String name, double runSpeed, double bikeSpeed, String type){
		this.name = name;
		this.type = type;
		this.runSpeed = runSpeed;
		this.bikeSpeed = bikeSpeed;
	}

	@Override
	public String disciplines() {
		return "I run, bike, then sometimes run again. In a long distance duathlon, I run 6.2 miles, bike 93 miles, then run 18.6 miles";
	}

	@Override
	public double bike() {
		return this.bikeSpeed;
	}

	@Override
	public double run() {
		return this.runSpeed;
	}
	
}// End duathlete class

class Aquathlete extends Athlete implements Runner, Swimmer{
	
	private double swimSpeed;
	private double runSpeed;
	
	Aquathlete(String name, double runSpeed, double swimSpeed, String type){
		this.name = name;
		this.type = type;
		this.runSpeed = runSpeed;
		this.swimSpeed = swimSpeed;
	}

	@Override
	public String disciplines() {
		return "I run, swim, then run again. In the Swedish OTILLO Championship, the race takes place over 24 islands and requires 6 miles of swimming between the islands and 40 miles of trail running.";
	}

	@Override
	public double Swim() {
		return this.swimSpeed;
	}

	@Override
	public double run() {
		return this.runSpeed;
	}
	
}//End Aquathlete class


class Marathoner extends Athlete implements Runner{
	
	private double runSpeed;
	
	Marathoner(String name, double runSpeed, String type){
		this.name = name;
		this.type = type;
		this.runSpeed = runSpeed;
	}

	@Override
	public String disciplines() {
		return "During a full marathon I run 26.2 miles!";
	}

	@Override
	public double run() {
		return this.runSpeed;
	}
}// End marathoner class