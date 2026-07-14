// ============================================================================
// Q3  (CSE 308 - B1)  ShakeShack
// Shakes: Chocolate_Shake, Coffee_Shake, Zero_Shake. All have a fixed base; the
// customer may optionally make it lactose-free (+60), add candy (+50) or cookies
// (+40). The customer only calls produceShake and never sees construction detail.
//
// PATTERN : BUILDER
//   A ShakeBuilder starts from a base shake type, then optional steps
//   (lactoseFree / addCandy / addCookies) mutate ingredients and price. build()
//   returns the finished immutable Shake. ShakeShack.produceShake(...) is the
//   Director-style facade so the customer stays ignorant of the steps.
//   (Only the SHAKES use the pattern; the O/E ordering loop is plain code.)
//
// SOLID :
//   - SRP : Shake holds data; ShakeBuilder handles step-by-step construction;
//           Order handles printing/totalling. Three responsibilities, three
//           classes.
//   - OCP : a new topping = one new builder method, existing shakes untouched.
//   - DIP : the ordering code depends on produceShake, not on constructors.
// ============================================================================

import java.util.ArrayList;
import java.util.List;

// ---------------- The product ------------------------------------------------
class Shake {
    final String name;
    final List<String> ingredients;   // base + added, in order
    final List<String> priceLines;    // human-readable price breakdown
    final int totalPrice;

    Shake(String name, List<String> ingredients, List<String> priceLines, int totalPrice) {
        this.name = name;
        this.ingredients = ingredients;
        this.priceLines = priceLines;
        this.totalPrice = totalPrice;
    }

    void print() {
        System.out.println("  * " + name);
        System.out.println("      Ingredients : " + String.join(", ", ingredients));
        for (String line : priceLines) System.out.println("      " + line);
        System.out.println("      Item total  : Tk " + totalPrice);
    }
}

// ---------------- The Builder ------------------------------------------------
class ShakeBuilder {
    private final String name;
    private final List<String> ingredients = new ArrayList<>();
    private final List<String> priceLines  = new ArrayList<>();
    private int price;

    // Constructor seeds the mandatory base of the chosen shake type.
    ShakeBuilder(String type) {
        this.name = type;
        switch (type) {
            case "Chocolate_Shake":
                price = 230;
                ingredients.add("milk"); ingredients.add("sugar");
                ingredients.add("chocolate syrup"); ingredients.add("chocolate ice cream");
                break;
            case "Coffee_Shake":
                price = 230;
                ingredients.add("milk"); ingredients.add("sugar");
                ingredients.add("chocolate syrup"); ingredients.add("chocolate ice cream");
                ingredients.add("coffee");
                break;
            case "Zero_Shake":
                price = 240;                                   // no sugar
                ingredients.add("milk");
                ingredients.add("chocolate syrup"); ingredients.add("chocolate ice cream");
                break;
            default:
                throw new IllegalArgumentException("Unknown shake type: " + type);
        }
        priceLines.add("Base price      : Tk " + price);
    }

    // Optional step: swap milk -> almond milk, +60.
    ShakeBuilder lactoseFree() {
        int idx = ingredients.indexOf("milk");
        if (idx >= 0) ingredients.set(idx, "almond milk");
        price += 60;
        priceLines.add("+ Lactose-free  : Tk 60  (almond milk instead of milk)");
        return this;
    }

    // Optional step: candy on top, +50.
    ShakeBuilder addCandy() {
        ingredients.add("candy (topping)");
        price += 50;
        priceLines.add("+ Candy topping : Tk 50");
        return this;
    }

    // Optional step: cookies on top, +40.
    ShakeBuilder addCookies() {
        ingredients.add("cookies (topping)");
        price += 40;
        priceLines.add("+ Cookies topping: Tk 40");
        return this;
    }

    Shake build() {
        return new Shake(name, new ArrayList<>(ingredients), new ArrayList<>(priceLines), price);
    }
}

// ---------------- Director-style facade : the ONLY thing the customer uses ----
class ShakeShack {
    static Shake produceShake(String type, boolean lactoseFree, boolean candy, boolean cookies) {
        ShakeBuilder b = new ShakeBuilder(type);
        if (lactoseFree) b.lactoseFree();
        if (candy)       b.addCandy();
        if (cookies)     b.addCookies();
        return b.build();
    }
}

// ---------------- One customer order (open with O, close with E) -------------
class Order {
    private final List<Shake> shakes = new ArrayList<>();
    void add(Shake s) { shakes.add(s); }

    void printReceipt(int orderNo) {
        System.out.println("Order #" + orderNo + " -----------------------------");
        int total = 0;
        for (Shake s : shakes) { s.print(); total += s.totalPrice; }
        System.out.println("  ORDER TOTAL   : Tk " + total);
        System.out.println("--------------------------------------------\n");
    }
}

public class ShakeShackDemo {

    public static void main(String[] args) {
        // The problem allows scripted test cases. Each "O ... E" block is one
        // sequential order. (Swap this array for a Scanner to read real input.)
        String[] commands = {
            "O",
            "Chocolate_Shake",                 // plain
            "Coffee_Shake:lactose",            // lactose-free
            "Zero_Shake:candy,cookies",        // both toppings
            "E",
            "O",
            "Chocolate_Shake:lactose,candy",   // lactose-free + candy
            "E"
        };

        Order current = null;
        int orderNo = 0;

        for (String cmd : commands) {
            if (cmd.equals("O")) {                       // open an order
                current = new Order();
                orderNo++;
            } else if (cmd.equals("E")) {                // close & print
                if (current != null) current.printReceipt(orderNo);
                current = null;
            } else if (current != null) {                // a shake line
                String type = cmd.contains(":") ? cmd.substring(0, cmd.indexOf(':')) : cmd;
                String opts = cmd.contains(":") ? cmd.substring(cmd.indexOf(':') + 1) : "";
                boolean lactose = opts.contains("lactose");
                boolean candy   = opts.contains("candy");
                boolean cookies = opts.contains("cookies");
                current.add(ShakeShack.produceShake(type, lactose, candy, cookies));
            }
        }
    }
}
