// ===================================================================
// A2 : Travel-agency holiday packages  ->  BUILDER PATTERN (+ Director)
// -------------------------------------------------------------------
// A HolidayPackage is a COMPLEX object built in several steps
// (flight -> hotel -> activity). Builder separates the *construction
// process* from the *representation*: the SAME step sequence, driven
// by the Director, produces DIFFERENT packages depending on which
// concrete builder is plugged in.
// ===================================================================

// ---- Product ----
class HolidayPackage {
    private String flight;
    private String hotel;
    private String activity;

    public void setFlight(String flight)     { this.flight = flight; }
    public void setHotel(String hotel)        { this.hotel = hotel; }
    public void setActivity(String activity)  { this.activity = activity; }

    public void show() {
        System.out.println("Holiday Package:");
        System.out.println("   Flight   : " + flight);
        System.out.println("   Hotel    : " + hotel);
        System.out.println("   Activity : " + activity);
    }
}

// ---- Builder abstraction: the construction steps ----
interface PackageBuilder {
    void buildFlight();
    void buildHotel();
    void buildActivity();
    HolidayPackage getPackage();
}

// ---- Concrete builder 1 ----
class RelaxationBuilder implements PackageBuilder {
    private HolidayPackage pkg = new HolidayPackage();
    public void buildFlight()   { pkg.setFlight("Business Class Flight"); }
    public void buildHotel()    { pkg.setHotel("5-Star Resort"); }
    public void buildActivity() { pkg.setActivity("Spa Treatment"); }
    public HolidayPackage getPackage() { return pkg; }
}

// ---- Concrete builder 2 ----
class AdventureBuilder implements PackageBuilder {
    private HolidayPackage pkg = new HolidayPackage();
    public void buildFlight()   { pkg.setFlight("Economy Flight"); }
    public void buildHotel()    { pkg.setHotel("Mountain Cabin"); }
    public void buildActivity() { pkg.setActivity("Hiking Tour"); }
    public HolidayPackage getPackage() { return pkg; }
}

// ---- Director: knows the ORDER of steps, not the concrete details ----
class TravelAgency {
    public HolidayPackage construct(PackageBuilder builder) {
        builder.buildFlight();
        builder.buildHotel();
        builder.buildActivity();
        return builder.getPackage();
    }
}

public class A2_HolidayPackageBuilder {
    public static void main(String[] args) {
        TravelAgency agency = new TravelAgency();

        // Same construction process, two different representations:
        HolidayPackage relax = agency.construct(new RelaxationBuilder());
        relax.show();

        HolidayPackage adventure = agency.construct(new AdventureBuilder());
        adventure.show();
    }
}
