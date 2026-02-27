import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;

public class WeibelJosephAssignment4 {

	public static void main(String[] args) {
		//Declare and initialize variables for reading a file
		int loadingDockArraySizeInt = 0;
		int tarmacArraySizeInt = 0;
		String arraySizeString = "";
		
		try {
			//Create a BufferedReader object that reads the specified text file
			BufferedReader reader = new BufferedReader(new FileReader("FedExPlanes.txt"));
			arraySizeString = reader.readLine();
			reader.close();
		} catch(IOException e) {
			e.printStackTrace();
		}
		loadingDockArraySizeInt = Integer.parseInt(arraySizeString.trim());
		
		try {
			//Create a BufferedReader object that reads the specified text file
			BufferedReader reader = new BufferedReader(new FileReader("FedExTrucks.txt"));
			arraySizeString = reader.readLine();
			reader.close();
		} catch(IOException e) {
			e.printStackTrace();
		}
		tarmacArraySizeInt = Integer.parseInt(arraySizeString.trim());
		
		CargoTerminal cargoTerminal = new CargoTerminal(tarmacArraySizeInt, loadingDockArraySizeInt);
		
		fillArrayFromText("FedExTrucks.txt", cargoTerminal);
		fillArrayFromText("FedExPlanes.txt", cargoTerminal);
		cargoTerminal.displayTrucksAndPlanes();
		printTarmacStatus(cargoTerminal);
	}//End main method
	
	public static void printTarmacStatus (CargoTerminal terminal) {
		ArrayList<PlaneReport> planeReportArrayList = new ArrayList<PlaneReport>();
		

		for(int i = 1; i < terminal.getTarmacSize(); i++) {
			CargoPlane cargoPlane = terminal.getCargoPlane(i);
			
			if (cargoPlane != null) {
				PlaneReport planeReport = new PlaneReport(i, cargoPlane.getFlightNumber(), cargoPlane.getType(), cargoPlane.getCapacity(), cargoPlane.getdestinationCity());
				planeReportArrayList.add(planeReport);
			}
		}
		Collections.sort(planeReportArrayList);
		
		System.out.println("**********************************************************************************");
		System.out.println("\t\t\t\tTarmac Status");
		System.out.println("\t\t\t(Lowest to Highest Capacity)");
		System.out.println("**********************************************************************************");
		System.out.println("Flight\t\tStand\t\tDeparting To\t\tType\t\tCapacity(lbs)");
		System.out.println("----------------------------------------------------------------------------------");
		
		for(PlaneReport plane : planeReportArrayList) {
			System.out.println(plane.print());
		}
	}
	
	static void fillArrayFromText(String fileName, CargoTerminal cargoTerminalInstance) {
		try {
			//Create a file reader object again to read the same file
			BufferedReader reader = new BufferedReader(new FileReader(fileName));
			reader.readLine();
			String line;

			//Iterate over the lines in the file until there are no more lines left to read
			while ((line = reader.readLine()) != null) {
				//Split the line read into different sections based off a delimiter of a space
				if(fileName.equals("FedExTrucks.txt")) {
					String[] sections = line.split(" ");					
					
					int space = Integer.parseInt(sections[0]);
					int truckNumber = Integer.parseInt(sections[1]);
					String destinationCity = sections[2];
					
					SemiTruck semiTruck = new SemiTruck(truckNumber, destinationCity);
					cargoTerminalInstance.addSemiTruck(space, semiTruck);
				}
				else if(fileName.equals("FedExPlanes.txt")) {
					String[] sections = line.split(" ");
				
					int standNumber = Integer.parseInt(sections[0]);
					int flightNumber = Integer.parseInt(sections[1]);
					String typeOfPlane = sections[2];
					double capacity = Double.parseDouble(sections[3]);
					String destinationCity = sections[4];
					
					CargoPlane cargoPlane = new CargoPlane(flightNumber, typeOfPlane, capacity, destinationCity);
					cargoTerminalInstance.addCargoPlane(standNumber, cargoPlane);
					
				}
			}
			reader.close();
		} catch(IOException e) {
			e.printStackTrace();
		}
	} //End fill array from text method
	
}// End main Class


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
		return loadingDock[dock];
	}
	public CargoPlane getCargoPlane (int stand) {
		return tarmac[stand];
	}
	public void displayTrucksAndPlanes() {
	    System.out.println("Loading semi-trucks and planes into cargo terminal...\n");
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


class CargoPlane{
	private int flightNumber;
	private String type;
	private double capacity;
	private String destinationCity;
	
	public CargoPlane(int flightNumber, String type, double capacity, String destinationCity){
		this.flightNumber = flightNumber;
		this.type = type;
		this.capacity = capacity;
		this.destinationCity = destinationCity;
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
}


class PlaneReport implements Printable, Comparable<PlaneReport>{
	private int stand;
	private int flightNumber;
	private String type;
	private double capacity;
	private String destinationCity;
	
	public PlaneReport(int stand, int flightNumber, String type, double capacity, String destinationCity) {
		this.stand = stand;
		this.flightNumber = flightNumber;
		this.type = type;
		this.capacity = capacity;
		this.destinationCity = destinationCity;
	}
	
	@Override
	public String print() {
		return String.format("%4d\t\t%2d\t\t%-15s\t\t%-10s\t%.2f", flightNumber, stand, destinationCity, type, capacity);
	}

	@Override
	public int compareTo(PlaneReport otherReport) {
		return (Integer)Double.compare(this.capacity, otherReport.capacity); 
	}
}

interface Printable{
	String print();
}