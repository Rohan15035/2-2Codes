interface Transport {
    public void deliver();
}

class Truck implements Transport {

    @Override
    public void deliver() {
        System.out.println("Truck");
    }
}

class Ship implements Transport {
    @Override
    public void deliver() {
        System.out.println("Ship");
    }
}

class TransportFactory {

    public Transport create(String s) {
        if (s == null)
            throw new IllegalArgumentException("Null string");
        switch (s.toLowerCase()) {
            case "road":
                return new Truck();

            case "sea":
                return new Ship();
            default:
                throw new IllegalArgumentException();

        }
    }
}

public class demoA1 {
    public static void main(String[] args) {
        TransportFactory shop = new TransportFactory();
        Transport t = shop.create("road");
        Transport s = shop.create("sea");
        t.deliver();
        s.deliver();

    }

}
