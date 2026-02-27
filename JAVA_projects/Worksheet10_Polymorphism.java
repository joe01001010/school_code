public class Worksheet10_Polymorphism {
	public static void main(String[] args) {
// Add code here to create array of 5 automobiles
		Automobile[] automobiles = new Automobile[5];
		automobiles[0] = new SUV("Chevy");
		automobiles[1] = new SUV("Toyota");
		automobiles[2] = new SUV("Ford");
		automobiles[3] = new SportsCar("BMW");
		automobiles[4] = new SportsCar("Audi");
// Then iterate through the array printing the manufacturer
		for (int i = 0;i < 5; i++) {
			System.out.printf("%s\n", automobiles[i].getManufacturer());
		}
	}
} //Worksheet10

class Automobile {
	String manufacturer;
	public Automobile(String manufacturer) {
			this.manufacturer = manufacturer;
	}
	public String getManufacturer() {
		return manufacturer;
	}
}

class SUV extends Automobile {
	public SUV(String manufacturer) {
		super(manufacturer);
	}
}

class SportsCar extends Automobile {
	public SportsCar(String manufacturer) {
			super(manufacturer);
	}
}