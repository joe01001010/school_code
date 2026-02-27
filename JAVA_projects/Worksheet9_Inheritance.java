public class Worksheet9_Inheritance {
	public static void main(String[] args) {
		
// Create some SUVs and some Sport Cars
		SUV aFordSUV = new SUV("Ford");
		SportsCar aBMW = new SportsCar("BMW");
		SUV aChevySUV = new SUV("Chevy");
		System.out.println(aFordSUV.getManufacturer());
		System.out.println(aBMW.getManufacturer());
		System.out.println(aChevySUV.getManufacturer());
	}
} //Worksheet9

class Automobile {
	private String manufacturer;
	
	public Automobile(String manufacturer) {
		this.manufacturer = manufacturer;
	}
	
	public void setManufacturer(String manufacturer) {
		this.manufacturer = manufacturer;
	}
	
	public String getManufacturer() {
		return this.manufacturer;
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