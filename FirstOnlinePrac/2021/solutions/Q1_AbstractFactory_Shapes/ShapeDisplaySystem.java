// ============================================================================
// Q1  (CSE 308 - A1)
// Display & print shapes at a resolution that depends on the computer running
// the system. Each computer has its OWN CPU and MMU that must be used together.
//
// PATTERN : ABSTRACT FACTORY
//   Each "Computer" is a concrete factory that produces a *family* of related
//   products meant to be used together: a matching CPU and a matching MMU.
//   The client talks only to the abstract Computer / CPU / MMU types, so it
//   never hard-codes ComputerA/B/C.
//
// SOLID :
//   - DIP : the client depends on abstractions (Computer, CPU, MMU), not on any
//           concrete class.
//   - OCP : adding a ComputerD = writing new classes only; no existing code
//           changes.
//   - SRP : Shape knows geometry, CPU knows rendering, MMU knows memory.
//   - LSP : any concrete CPU/MMU can stand in for its interface.
//
// "Be careful about how much demand it places on the computer" -> each computer
// creates its CPU/MMU lazily and caches them (created once, reused).
// ============================================================================

import java.util.HashMap;
import java.util.Map;

// ---------------- Product family #1 : the shapes to be displayed -------------
interface Shape {
    String name();
    double area();        // "surface area"
    double perimeter();
}

class Circle implements Shape {
    private final double r;
    Circle(double r) {
        if (r <= 0) throw new IllegalArgumentException("Circle radius must be > 0");
        this.r = r;
    }
    public String name()      { return "Circle"; }
    public double area()      { return Math.PI * r * r; }
    public double perimeter() { return 2 * Math.PI * r; }
}

class Square implements Shape {
    private final double s;
    Square(double s) {
        if (s <= 0) throw new IllegalArgumentException("Square side must be > 0");
        this.s = s;
    }
    public String name()      { return "Square"; }
    public double area()      { return s * s; }
    public double perimeter() { return 4 * s; }
}

class Rectangle implements Shape {
    private final double w, h;
    Rectangle(double w, double h) {
        if (w <= 0 || h <= 0) throw new IllegalArgumentException("Rectangle sides must be > 0");
        this.w = w; this.h = h;
    }
    public String name()      { return "Rectangle"; }
    public double area()      { return w * h; }
    public double perimeter() { return 2 * (w + h); }
}

// ---------------- Abstract products created by the factory -------------------
interface CPU {
    String model();
    String render(Shape shape, String resolution);
}

interface MMU {
    String model();
    String allocate(String resolution);
}

// ---------------- Concrete products : Computer A -----------------------------
class CpuA implements CPU {
    public String model() { return "CPU-A"; }
    public String render(Shape s, String res) { return "CPU-A draws " + s.name() + " @ " + res; }
}
class MmuA implements MMU {
    public String model() { return "MMU-A"; }
    public String allocate(String res) { return "MMU-A reserved a " + res + " framebuffer"; }
}

// ---------------- Concrete products : Computer B -----------------------------
class CpuB implements CPU {
    public String model() { return "CPU-B"; }
    public String render(Shape s, String res) { return "CPU-B draws " + s.name() + " @ " + res; }
}
class MmuB implements MMU {
    public String model() { return "MMU-B"; }
    public String allocate(String res) { return "MMU-B reserved a " + res + " framebuffer"; }
}

// ---------------- Concrete products : Computer C -----------------------------
class CpuC implements CPU {
    public String model() { return "CPU-C"; }
    public String render(Shape s, String res) { return "CPU-C draws " + s.name() + " @ " + res; }
}
class MmuC implements MMU {
    public String model() { return "MMU-C"; }
    public String allocate(String res) { return "MMU-C reserved a " + res + " framebuffer"; }
}

// ---------------- The Abstract Factory ---------------------------------------
interface Computer {
    String name();
    String resolution();
    CPU getCPU();     // lazily created + cached (careful about resource demand)
    MMU getMMU();
}

// Small base class to cache CPU/MMU so we do not re-create them on every draw.
abstract class AbstractComputer implements Computer {
    private CPU cpu;
    private MMU mmu;
    protected abstract CPU makeCPU();
    protected abstract MMU makeMMU();
    public CPU getCPU() { if (cpu == null) cpu = makeCPU(); return cpu; }
    public MMU getMMU() { if (mmu == null) mmu = makeMMU(); return mmu; }
}

class ComputerA extends AbstractComputer {
    public String name()       { return "ComputerA"; }
    public String resolution() { return "200x200"; }
    protected CPU makeCPU()    { return new CpuA(); }
    protected MMU makeMMU()    { return new MmuA(); }
}
class ComputerB extends AbstractComputer {
    public String name()       { return "ComputerB"; }
    public String resolution() { return "350x250"; }
    protected CPU makeCPU()    { return new CpuB(); }
    protected MMU makeMMU()    { return new MmuB(); }
}
class ComputerC extends AbstractComputer {
    public String name()       { return "ComputerC"; }
    public String resolution() { return "550x430"; }
    protected CPU makeCPU()    { return new CpuC(); }
    protected MMU makeMMU()    { return new MmuC(); }
}

// Chooses the correct factory from the computer name (the only place that
// mentions concrete factories -> keeps the rest of the code OCP-friendly).
class ComputerProvider {
    static Computer forName(String computerName) {
        switch (computerName) {
            case "ComputerA": return new ComputerA();
            case "ComputerB": return new ComputerB();
            case "ComputerC": return new ComputerC();
            default: throw new IllegalArgumentException("Unknown computer: " + computerName);
        }
    }
}

// ---------------- Client : renders a shape using ONE computer's family -------
public class ShapeDisplaySystem {

    static void display(String computerName, Shape shape) {
        System.out.println("=== Request: " + shape.name() + " on " + computerName + " ===");
        try {
            Computer computer = ComputerProvider.forName(computerName);   // pick factory
            CPU cpu = computer.getCPU();                                  // matching family...
            MMU mmu = computer.getMMU();                                  // ...used together
            String res = computer.resolution();

            System.out.println("Initialized " + cpu.model() + " + " + mmu.model()
                    + " on " + computer.name());
            System.out.println("  " + mmu.allocate(res));
            System.out.println("  " + cpu.render(shape, res));
            System.out.printf ("  Shape      : %s%n", shape.name());
            System.out.printf ("  Resolution : %s%n", res);
            System.out.printf ("  Area       : %.2f%n", shape.area());
            System.out.printf ("  Perimeter  : %.2f%n", shape.perimeter());
        } catch (IllegalArgumentException ex) {
            System.out.println("  [Rejected] " + ex.getMessage());
        }
        System.out.println();
    }

    public static void main(String[] args) {
        // ---- Normal test cases (computer name, shape, parameters) ----
        display("ComputerA", new Circle(5));
        display("ComputerB", new Rectangle(4, 6));
        display("ComputerC", new Square(3));

        // ---- Boundary conditions ----
        display("ComputerX", new Square(2));          // unknown computer
        try {
            display("ComputerA", new Circle(-1));     // invalid parameter
        } catch (IllegalArgumentException ex) {
            System.out.println("  [Rejected] " + ex.getMessage() + "\n");
        }
    }
}
