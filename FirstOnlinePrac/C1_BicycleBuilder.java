// ===================================================================
// C1 : Customized bicycle manufacturer  ->  BUILDER PATTERN (+ Director)
// -------------------------------------------------------------------
// A Bicycle is assembled step-by-step: frame -> gears -> tires.
// A Director owns that sequence; concrete builders supply the parts.
// The client just asks the director for a model and receives the
// fully assembled product, unaware of the assembly details.
// ===================================================================

// ---- Product ----
class Bicycle {
    private String frame;
    private String gearSystem;
    private String tireType;

    public void setFrame(String frame)         { this.frame = frame; }
    public void setGearSystem(String gears)     { this.gearSystem = gears; }
    public void setTireType(String tires)       { this.tireType = tires; }

    public void show() {
        System.out.println("Bicycle assembled:");
        System.out.println("   Frame : " + frame);
        System.out.println("   Gears : " + gearSystem);
        System.out.println("   Tires : " + tireType);
    }
}

// ---- Builder abstraction: the assembly steps ----
interface BicycleBuilder {
    void buildFrame();
    void buildGears();
    void buildTires();
    Bicycle getBicycle();
}

// ---- Concrete builder 1 ----
class CommuterBuilder implements BicycleBuilder {
    private Bicycle bike = new Bicycle();
    public void buildFrame() { bike.setFrame("Aluminum Frame"); }
    public void buildGears() { bike.setGearSystem("Single Speed Gear"); }
    public void buildTires() { bike.setTireType("Road Tires"); }
    public Bicycle getBicycle() { return bike; }
}

// ---- Concrete builder 2 ----
class MountainBeastBuilder implements BicycleBuilder {
    private Bicycle bike = new Bicycle();
    public void buildFrame() { bike.setFrame("Carbon Fiber Frame"); }
    public void buildGears() { bike.setGearSystem("12-Speed Gear"); }
    public void buildTires() { bike.setTireType("Off-road Grip Tires"); }
    public Bicycle getBicycle() { return bike; }
}

// ---- Director: fixes the construction ORDER ----
class BicycleDirector {
    public Bicycle construct(BicycleBuilder builder) {
        builder.buildFrame();   // step 1
        builder.buildGears();   // step 2
        builder.buildTires();   // step 3
        return builder.getBicycle();
    }
}

public class C1_BicycleBuilder {
    public static void main(String[] args) {
        BicycleDirector director = new BicycleDirector();

        // Client only names a model; director returns the finished bike.
        Bicycle commuter = director.construct(new CommuterBuilder());
        commuter.show();

        Bicycle mountain = director.construct(new MountainBeastBuilder());
        mountain.show();
    }
}
