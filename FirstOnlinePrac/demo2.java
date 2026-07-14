class cycle {

    private String frame;
    private String gear;
    private String tire;

    public void setFrame(String s) {
        this.frame = s;
    }

    public void setGear(String s) {
        this.gear = s;
    }

    public void setTire(String s) {
        this.tire = s;
    }

}

interface builder {
    public void buildTire();

    public void buildGear();

    public void buildFrame();

    public cycle returnCycle();
}

class CommuterBuilder implements builder {

    cycle c;

    CommuterBuilder() {
        c = new cycle();
    }

    @Override
    public void buildFrame() {
        // TODO Auto-generated method stub
        c.setFrame("Aluminium");

    }

    @Override
    public void buildGear() {
        c.setGear("Single Speed");

    }

    @Override
    public void buildTire() {
        c.setTire("Road");
    }

    @Override
    public cycle returnCycle() {
        return c;
    }
}

class MountainBuilder implements builder {

    cycle c;

    MountainBuilder() {
        c = new cycle();
    }

    @Override
    public void buildFrame() {
        // TODO Auto-generated method stub
        c.setFrame("Carbon Fiber");

    }

    @Override
    public void buildGear() {
        c.setGear("12-Speed");

    }

    @Override
    public void buildTire() {
        c.setTire("Off-Road");
    }

    @Override
    public cycle returnCycle() {
        return c;
    }
}

class director {

    public cycle build(builder b) {
        b.buildFrame();
        b.buildGear();
        b.buildTire();
        return b.returnCycle();

    }

}

public class demo2 {
    public static void main(String[] args) {
        director shop = new director();
        cycle c1 = shop.build(new CommuterBuilder());
        cycle c2 = shop.build(new MountainBuilder());

    }

}
