// ============================================================================
// Q2  (CSE 308 - A2)
// Three manufacturers: Boeing, AirBus, Safran. Each builds an Airplane from its
// OWN matching Engine and Wing (you must never mix a Boeing engine with an
// AirBus wing).
//
// PATTERN : ABSTRACT FACTORY
//   Each manufacturer is a concrete factory that produces a whole family of
//   compatible parts (Engine + Wing) and assembles the Airplane. The client
//   only knows the abstract AirplaneFactory and gets back an Airplane.
//
// SOLID :
//   - DIP : client depends on AirplaneFactory / Airplane / Engine / Wing.
//   - OCP : a new manufacturer = a new factory + parts, no edits to the client.
//   - LSP : every concrete factory is usable wherever AirplaneFactory is.
// ============================================================================

// ---------------- Abstract parts (product family) ----------------------------
interface Engine { String describe(); }
interface Wing   { String describe(); }

// ---------------- Boeing parts -----------------------------------------------
class BoeingEngine implements Engine { public String describe() { return "Boeing turbofan engine"; } }
class BoeingWing   implements Wing   { public String describe() { return "Boeing swept wing"; } }

// ---------------- AirBus parts -----------------------------------------------
class AirBusEngine implements Engine { public String describe() { return "AirBus geared turbofan engine"; } }
class AirBusWing   implements Wing   { public String describe() { return "AirBus sharklet wing"; } }

// ---------------- Safran parts -----------------------------------------------
class SafranEngine implements Engine { public String describe() { return "Safran LEAP engine"; } }
class SafranWing   implements Wing   { public String describe() { return "Safran composite wing"; } }

// ---------------- The product being assembled --------------------------------
class Airplane {
    private final String manufacturer;
    private final Engine engine;
    private final Wing wing;

    Airplane(String manufacturer, Engine engine, Wing wing) {
        this.manufacturer = manufacturer;
        this.engine = engine;
        this.wing = wing;
    }

    void printDetails() {
        System.out.println("Airplane by " + manufacturer);
        System.out.println("  Engine : " + engine.describe());
        System.out.println("  Wing   : " + wing.describe());
    }
}

// ---------------- The Abstract Factory ---------------------------------------
interface AirplaneFactory {
    String companyName();
    Engine createEngine();
    Wing   createWing();

    // Assembly is identical for everyone -> a default method keeps each factory
    // focused only on WHICH parts to build (SRP + no duplication).
    default Airplane createAirplane() {
        return new Airplane(companyName(), createEngine(), createWing());
    }
}

// ---------------- Concrete factories -----------------------------------------
class BoeingFactory implements AirplaneFactory {
    public String companyName()  { return "Boeing"; }
    public Engine createEngine() { return new BoeingEngine(); }
    public Wing   createWing()   { return new BoeingWing(); }
}
class AirBusFactory implements AirplaneFactory {
    public String companyName()  { return "AirBus"; }
    public Engine createEngine() { return new AirBusEngine(); }
    public Wing   createWing()   { return new AirBusWing(); }
}
class SafranFactory implements AirplaneFactory {
    public String companyName()  { return "Safran"; }
    public Engine createEngine() { return new SafranEngine(); }
    public Wing   createWing()   { return new SafranWing(); }
}

// ---------------- Client -----------------------------------------------------
public class AirplaneFactoryDemo {

    // Picks the right factory from the user's preferred company name.
    static AirplaneFactory factoryFor(String company) {
        switch (company.toLowerCase()) {
            case "boeing": return new BoeingFactory();
            case "airbus": return new AirBusFactory();
            case "safran": return new SafranFactory();
            default: throw new IllegalArgumentException("Unknown company: " + company);
        }
    }

    static void order(String company) {
        System.out.println("--- Customer prefers: " + company + " ---");
        try {
            AirplaneFactory factory = factoryFor(company);   // initialize correct company
            Airplane plane = factory.createAirplane();       // build matched-part airplane
            plane.printDetails();
        } catch (IllegalArgumentException ex) {
            System.out.println("  [Rejected] " + ex.getMessage());
        }
        System.out.println();
    }

    public static void main(String[] args) {
        order("Boeing");
        order("AirBus");
        order("Safran");
        order("Cessna");   // boundary: unknown company
    }
}
