/*
Name: Joseph Weibel
Class: 2024Sp CS 1450 003
Section: 1
Due: Mar 18, 2024
Description: Assignment #7
This program will be a continuation of programming assignment 4 and will move the plane and cargo truck objects out of the terminal.
This will involve new objects like taxiWay, airTrafficController, and runway. The planes will move in a priority based off the cargo
inside the cargoPlane.
*/

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.PriorityQueue;
import java.util.Queue;

public class WeibelJosephAssignment4 {

	public static void main(String[] args) {
		//Declare and initialize variables for reading a file
		int loadingDockArraySizeInt = 0;
		int tarmacArraySizeInt = 0;
		String arraySizeString = "";
		
		try {
			//Create a BufferedReader object that reads the specified text file
			BufferedReader reader = new BufferedReader(new FileReader("FedExPlanes7.txt"));
			arraySizeString = reader.readLine();
			reader.close();
		} catch(IOException e) {
			e.printStackTrace();
		}
		loadingDockArraySizeInt = Integer.parseInt(arraySizeString.trim());
		
		try {
			//Create a BufferedReader object that reads the specified text file
			BufferedReader reader = new BufferedReader(new FileReader("FedExTrucks7.txt"));
			arraySizeString = reader.readLine();
			reader.close();
		} catch(IOException e) {
			e.printStackTrace();
		}
		tarmacArraySizeInt = Integer.parseInt(arraySizeString.trim());
		
		//Used to invoke constructor to create a cargo terminal
		CargoTerminal cargoTerminal = new CargoTerminal(tarmacArraySizeInt, loadingDockArraySizeInt);
		
		//Fill array method expexts a filename and a cargoterminal object as arguments
		fillArrayFromText("FedExTrucks7.txt", cargoTerminal);
		fillArrayFromText("FedExPlanes7.txt", cargoTerminal);
		System.out.println("Loading semi-trucks and planes into cargo terminal...\n");
		cargoTerminal.displayTrucksAndPlanes();
		
		//create airtraffic controller object and use that to move the planes
		AirTrafficController controlTower = new AirTrafficController();
		Taxiways taxiways = new Taxiways();
		//move planes from cargo terminal to taxiway
		controlTower.movePlanesToTaxiways(cargoTerminal, taxiways);
		
		System.out.println("Show empty tarmac in cargo terminal...\n");
		//Showing the cargo terminal has no planes
		cargoTerminal.displayTrucksAndPlanes();
		
		Runway runway = new Runway();
		//Move the planes from the taxiways to the runway
		controlTower.movePlanesToRunway(taxiways, runway);
		
		//Remove the planes from the runway and clear them for takeoff
		controlTower.clearedForTakeoff(runway);
		
	}//End main method
	
	static void fillArrayFromText(String fileName, CargoTerminal cargoTerminalInstance) {
		try {
			//Create a file reader object again to read the same file
			BufferedReader reader = new BufferedReader(new FileReader(fileName));
			reader.readLine();
			String line;

			//Iterate over the lines in the file until there are no more lines left to read
			while ((line = reader.readLine()) != null) {
				//Split the line read into different sections based off a delimiter of a space
				if(fileName.equals("FedExTrucks7.txt")) {
					String[] sections = line.split(" ");					
					
					int space = Integer.parseInt(sections[0]);
					int truckNumber = Integer.parseInt(sections[1]);
					String destinationCity = sections[2];
					
					SemiTruck semiTruck = new SemiTruck(truckNumber, destinationCity);
					cargoTerminalInstance.addSemiTruck(space, semiTruck);
				}
				else if(fileName.equals("FedExPlanes7.txt")) {
					String[] sections = line.split(" ");
				
					int standNumber = Integer.parseInt(sections[0]);
					String cargoType = sections[1];
					int flightNumber = Integer.parseInt(sections[2]);
					String typeOfPlane = sections[3];
					double capacity = Double.parseDouble(sections[4]);
					String destinationCity = sections[5];
					
					CargoPlane cargoPlane = new CargoPlane(flightNumber, typeOfPlane, capacity, destinationCity, cargoType);
					cargoTerminalInstance.addCargoPlane(standNumber, cargoPlane);
					
				}
			}
			reader.close();
		} catch(IOException e) {
			e.printStackTrace();
		}
	} //End fill array from text method
	
}// End main Class


class AirTrafficController{
	public void movePlanesToTaxiways (CargoTerminal cargoTerminal, Taxiways taxiways) {
		System.out.println("Control Tower: Moving planes from cargo terminal to taxiways:");
		System.out.println("--------------------------------------------------------------------");
		for(int i = 0; i < cargoTerminal.getNumberStands(); i++) {
			CargoPlane plane = cargoTerminal.removeCargoPlane(i);
			
			if(plane != null) {
				if ("medical".equals(plane.getCargoType())) {
					System.out.printf("Moved to taxiway Urgent  \tflight:\t%d\t%s   \t%s\n", plane.getFlightNumber(), plane.getdestinationCity(), plane.getCargoType());
					taxiways.addPlaneToUrgentTaxiway(plane);
				}
				else if ("animals".equals(plane.getCargoType())) {
					System.out.printf("Moved to taxiway Urgent  \tflight:\t%d\t%s   \t%s\n", plane.getFlightNumber(), plane.getdestinationCity(), plane.getCargoType());
					taxiways.addPlaneToUrgentTaxiway(plane);
				}
				else {
					System.out.printf("Moved to taxiway Standard\tflight:\t%d\t%s   \t%s\n", plane.getFlightNumber(), plane.getdestinationCity(), plane.getCargoType());
					taxiways.addPlaneToStandardTaxiway(plane);
				}
			}
		}
		System.out.println("\n");
	}
	public void movePlanesToRunway (Taxiways taxiways, Runway runway) {
		ArrayList<CargoPlane> cargoPlaneWaiting = new ArrayList<CargoPlane>();
		
		System.out.println("Control Tower: Moving cargo planes from taxiways to runway");
		System.out.println("--------------------------------------------------------------------");
		while(!taxiways.isUrgentTaxiwayEmpty()) {
			CargoPlane plane = taxiways.removePlaneFromUrgentTaxiway();
			if ("medical".equals(plane.getCargoType())){
				runway.addPlaneToRunway(plane);
				System.out.printf("Moved to runway flight: %d\t%s   \t%s\n", plane.getFlightNumber(), plane.getdestinationCity(), plane.getCargoType());
			}
			else {
				cargoPlaneWaiting.add(plane);
			}
		}
		if(cargoPlaneWaiting != null) {
			for(CargoPlane plane : cargoPlaneWaiting) {
				runway.addPlaneToRunway(plane);
				System.out.printf("Moved to runway flight: %d\t%s   \t%s\n", plane.getFlightNumber(), plane.getdestinationCity(), plane.getCargoType());
			}
		}
		
		while(!taxiways.isStandardTaxiwayEmpty()) {
			CargoPlane plane = taxiways.removePlaneFromStandardTaxiway();
			runway.addPlaneToRunway(plane);
			System.out.printf("Moved to runway flight: %d\t%s   \t%s\n", plane.getFlightNumber(), plane.getdestinationCity(), plane.getCargoType());
		}
		System.out.println("\n");
	}
	public void clearedForTakeoff (Runway runway) {
		System.out.println("Control Tower: Ready for takeoff!");
		System.out.println("--------------------------------------------------------------------");
		
		while(!runway.isRunwayEmpty()) {
			CargoPlane plane = runway.removePlaneFromRunway();
			System.out.printf("Cleared for takeoff flight: %d\t%s   \t%s\n", plane.getFlightNumber(), plane.getdestinationCity(), plane.getCargoType());
		}
	}
}


class Runway{
	private Queue<CargoPlane> runway;
	
	public Runway() {
		this.runway = new LinkedList<>();
	}
	public boolean isRunwayEmpty() {
		return runway.isEmpty();
	}
	public void addPlaneToRunway(CargoPlane cargoPlane) {
		runway.add(cargoPlane);
	}
	public CargoPlane removePlaneFromRunway() {
		return runway.poll();
	}
}


class Taxiways{
	private PriorityQueue<CargoPlane> urgentTaxiway;
	private Queue<CargoPlane> standardTaxiway;
	
	public Taxiways() {
		urgentTaxiway = new PriorityQueue<>();
		standardTaxiway = new LinkedList<>();
	}
	
	public boolean isUrgentTaxiwayEmpty() {
		return urgentTaxiway.isEmpty();
	}
	public void addPlaneToUrgentTaxiway(CargoPlane cargoPlane) {
		urgentTaxiway.add(cargoPlane);
	}
	public CargoPlane removePlaneFromUrgentTaxiway() {
		return urgentTaxiway.poll();
	}
	
	public boolean isStandardTaxiwayEmpty() {
		return standardTaxiway.isEmpty();
	}
	public void addPlaneToStandardTaxiway(CargoPlane cargoPlane) {
		standardTaxiway.add(cargoPlane);
	}
	public CargoPlane removePlaneFromStandardTaxiway() {
		return standardTaxiway.poll();
	}
}


class CargoTerminal{
	private int numberDocks;
	private int numberStands;
	private SemiTruck[] loadingDock;
	private CargoPlane[] tarmac;
	
	public CargoTerminal(int numberDocks, int numberStands) {
		this.numberDocks = numberDocks;
		this.numberStands = numberStands;
		loadingDock = new SemiTruck[numberDocks];
		tarmac = new CargoPlane[numberStands];
	}
	public int getNumberDocks() {
		return this.numberDocks;
	}
	public int getNumberStands() {
		return this.numberStands;
	}
	public void addSemiTruck(int dock, SemiTruck semiTruck) {
		loadingDock[dock] = semiTruck;
	}
	public void addCargoPlane (int stand, CargoPlane plane) {
		tarmac[stand] = plane;
	}
	public SemiTruck getSemiTruck (int dock) {
		if(this.loadingDock[dock] != null) {
			return loadingDock[dock];
		}
		else {
			return null;
		}
	}
	public CargoPlane getCargoPlane (int stand) {
		if(this.tarmac[stand] != null) {
			return this.tarmac[stand];
		}
		else {
			return null;
		}
	}
	public CargoPlane removeCargoPlane(int stand) {
		CargoPlane removedPlane = tarmac[stand];
		tarmac[stand] = null;
		return removedPlane;
	}
	public void displayTrucksAndPlanes() {
	    for(int i = 1; i < this.numberDocks; i++) {
    		System.out.printf("Dock #%d\t\t", i);
    	}
	    System.out.println();
	    
	    for (int i = 1; i < this.numberDocks; i++) {
	        SemiTruck truck = this.getSemiTruck(i);
	        if (truck != null) {
	            System.out.printf("%d\t\t", truck.getTruckNumber());
	        } 
	        else {
	            System.out.print("------\t\t");
	        }
	    }
	    System.out.println();
	    
	    for(int i = 1; i < this.numberStands; i++) {
    		System.out.printf("Stand #%d\t", i);
    	}
	    System.out.println();
	    
	    for (int i = 1; i < this.numberStands; i++) {
	        CargoPlane plane = this.getCargoPlane(i);
	        if (plane != null) {
	            System.out.printf("%d\t\t", plane.getFlightNumber());
	        } else {
	            System.out.print("------\t\t");
	        }
	    }
	    System.out.println("\n\n");
	}
	public int getTarmacSize() {
		return tarmac.length;
	}
	public int getLoadingDockSize() {
		return loadingDock.length;
	}
}


class SemiTruck{
	private int truckNumber;
	private String destinationCity;
	
	public SemiTruck(int truckNumber, String destinationCity){
		this.truckNumber = truckNumber;
		this.destinationCity = destinationCity;
	}
	public int getTruckNumber() {
		return truckNumber;
	}
	public String getDestinationCity() {
		return destinationCity;
	}
}


class CargoPlane implements Comparable<CargoPlane>{
	private int flightNumber;
	private String cargoType;
	private String type;
	private double capacity;
	private String destinationCity;
	
	public CargoPlane(int flightNumber, String type, double capacity, String destinationCity, String cargoType){
		this.flightNumber = flightNumber;
		this.type = type;
		this.capacity = capacity;
		this.destinationCity = destinationCity;
		this.cargoType = cargoType;
	}
	public String getCargoType() {
		return cargoType;
	}
	public void setCargoType(String cargoType) {
		this.cargoType = cargoType;
	}
	public int getFlightNumber() {
		return flightNumber;
	}
	public String getType() {
		return type;
	}
	public double getCapacity() {
		return capacity;
	}
	public String getdestinationCity() {
		return destinationCity;
	}

    @Override
    public int compareTo(CargoPlane other) {
        // Define custom priority ordering
        if (this.cargoType.equals(other.cargoType)) {
            return 0;
        } 
        else if ("medical".equals(this.cargoType)) {
            return -1; 
        } 
        else if ("medical".equals(other.cargoType)) {
        	return 1;
        }
        else if ("animals".equals(this.cargoType)) {
            return "animals".equals(other.cargoType) ? 0 : -1;
        }
        else if ("animals".equals(other.cargoType)) {
            return 1;
        }
        else {
            return 0;
        }
    }
}