// ===================================================================
// A1 : Logistics transport  ->  FACTORY PATTERN
// -------------------------------------------------------------------
// The client only knows the delivery mode as a String ("Road"/"Sea").
// A factory decides WHICH concrete class to instantiate, so the client
// code never mentions Truck/Ship directly. Adding Airplane/Train later
// only touches the factory, not the client -> Open/Closed friendly.
// ===================================================================

// Common product interface
interface Transport {
    void deliver();
}

// Concrete products
class Truck implements Transport {
    public void deliver() {
        System.out.println("Delivering cargo by land in a Truck (Road).");
    }
}

class Ship implements Transport {
    public void deliver() {
        System.out.println("Delivering cargo by sea in a Ship (Sea).");
    }
}

// The Factory: encapsulates the object-creation decision in one place
class TransportFactory {
    public static Transport createTransport(String mode) {
        if (mode == null) {
            throw new IllegalArgumentException("Transport mode is required.");
        }
        switch (mode.toLowerCase()) {
            case "road": return new Truck();
            case "sea":  return new Ship();
            // To add "Air" later: add one case here + one new class.
            default:
                throw new IllegalArgumentException("Unknown transport mode: " + mode);
        }
    }
}

public class A1_TransportFactory {
    public static void main(String[] args) {
        // Client works only with the mode string and the Transport interface.
        Transport t1 = TransportFactory.createTransport("Road");
        t1.deliver();

        Transport t2 = TransportFactory.createTransport("Sea");
        t2.deliver();
    }
}
