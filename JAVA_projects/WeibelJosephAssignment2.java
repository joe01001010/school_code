import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class WeibelJosephAssignment2 {

	public static void main(String[] args) {
		String arraySizeString = "";
		int arraySizeInt = 0;
		
		try {
			BufferedReader reader = new BufferedReader(new FileReader("SeaTurtles.txt"));
			arraySizeString = reader.readLine();
			reader.close();
		} catch(IOException e) {
			e.printStackTrace();
		}
		
		arraySizeInt = Integer.parseInt(arraySizeString.trim());
		SeaTurtle[] seaTurtlesArray = new SeaTurtle[arraySizeInt];
		
		try {
			BufferedReader reader = new BufferedReader(new FileReader("SeaTurtles.txt"));
			reader.readLine();
			String line;
			int i = 0;
			
			while ((line = reader.readLine()) != null) {
				String[] sections = line.split(" ");
				String type = sections[0];
				int daysTracked = Integer.parseInt(sections[1]);
				double milesTraveled = Double.parseDouble(sections[2]);
				String name = sections[3];
				
				if (type.equals("lh")) {
					seaTurtlesArray[i] = new Loggerhead(name, daysTracked, milesTraveled);
				}
				else if (type.equals("hb")) {
					seaTurtlesArray[i] = new Hawksbill(name, daysTracked, milesTraveled);
				}
				else if (type.equals("lb")) {
					seaTurtlesArray[i] = new Leatherback(name, daysTracked, milesTraveled);
				}
				else if (type.equals("gt")) {
					seaTurtlesArray[i] = new GreenTurtle(name, daysTracked, milesTraveled);
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
		
		System.out.println("2018 Tour de Turtles");
		System.out.println("----------------------------------------------------------------------------------------------");
		System.out.println("Name\t\tType\t\tDays\t\tMiles\t\tThreats to Survival");
		System.out.println("    \t\t    \t\tTracked\t\tTraveled");
		System.out.println("----------------------------------------------------------------------------------------------");
		
		for(int i = 0; i < seaTurtlesArray.length; i++) {
			System.out.printf("%-9s\t%-12s\t%d\t\t%-8.2f\t%s\n", seaTurtlesArray[i].getName(), seaTurtlesArray[i].getType(), seaTurtlesArray[i].getDaysTracked(), seaTurtlesArray[i].getMilesTraveled(), seaTurtlesArray[i].threatsToSurvival());
		}
		
	}

}

class SeaTurtle{
	private String name;
	private String type;
	private int daysTracked;
	private double milesTraveled;
	
	public SeaTurtle(String name, String type, int daysTracked, double milesTraveled){
		this.type = type;
		this.daysTracked = daysTracked;
		this.milesTraveled = milesTraveled;
		this.name = name;
	}
	public String threatsToSurvival() {
		return ".50 Browning Machine Gun (.50 BMG)";
	}

	String getName() {
		return this.name;
	}
	String getType(){
		return this.type;
	}
	int getDaysTracked() {
		return this.daysTracked;
	}
	double getMilesTraveled() {
		return this.milesTraveled;
	}
}

class Loggerhead extends SeaTurtle{
	public Loggerhead(String name, int daysTracked, double milesTraveled) {
		super(name, "Loggerhead", daysTracked, milesTraveled);
	}
	
	@Override
	public String threatsToSurvival() {
		return "Loss of nesting habitat";
	}
}

class Hawksbill extends SeaTurtle{
	public Hawksbill(String name, int daysTracked, double milesTraveled) {
		super(name, "Hawksbill", daysTracked, milesTraveled);
	}
	
	@Override
	public String threatsToSurvival() {
		return "Harvesting of their shell";
	}
}

class Leatherback extends SeaTurtle{
	public Leatherback(String name, int daysTracked, double milesTraveled) {
		super(name, "Leatherback", daysTracked, milesTraveled);
	}
	
	@Override
	public String threatsToSurvival() {
		return "Plastic bag mistaken for jellyfish";
	}
}

class GreenTurtle extends SeaTurtle{
	public GreenTurtle(String name, int daysTracked, double milesTraveled) {
		super(name, "Green Turtle", daysTracked, milesTraveled);
	}
	
	@Override
	public String threatsToSurvival() {
		return "Commercial harvest for eggs & food";
	}
}