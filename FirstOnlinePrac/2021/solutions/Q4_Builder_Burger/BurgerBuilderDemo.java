// ============================================================================
// Q4  (CSE 308 - B2)  Burger restaurant
// Every burger has a mandatory base: 2 buns (20 each) + 1 regular patty (80).
// Optional add-ons may be repeated any number of times:
//   cheese 30, bbq sauce 20, salad 10, extra patty 80.
// Output the itemised order (base + added), each price, and the total.
//
// PATTERN : BUILDER
//   A BurgerBuilder starts with the fixed base, then fluent optional steps
//   (addCheese / addBbq / addSalad / addPatty) can be called repeatedly. build()
//   produces the finished Burger. Ideal when an object has a mandatory core plus
//   many optional, repeatable parts.
//
// SOLID :
//   - SRP : Burger stores the result & prints; BurgerBuilder assembles it.
//   - OCP : a new topping = one new builder method; the Burger class is stable.
//   - ISP : the builder exposes small, purpose-specific add* methods.
// ============================================================================

import java.util.ArrayList;
import java.util.List;

// ---------------- One line of the itemised bill ------------------------------
class LineItem {
    final String label;
    final int qty;
    final int unitPrice;
    LineItem(String label, int qty, int unitPrice) {
        this.label = label; this.qty = qty; this.unitPrice = unitPrice;
    }
    int subtotal() { return qty * unitPrice; }
    boolean isBase; // true for the mandatory base items
}

// ---------------- The product ------------------------------------------------
class Burger {
    private final List<LineItem> items;
    Burger(List<LineItem> items) { this.items = items; }

    void printOrder() {
        System.out.println("Burger order --------------------------------");
        System.out.println("  Base ingredients:");
        printGroup(true);
        System.out.println("  Added ingredients:");
        boolean anyAdded = printGroup(false);
        if (!anyAdded) System.out.println("      (none)");
        int total = items.stream().mapToInt(LineItem::subtotal).sum();
        System.out.println("  TOTAL PRICE : Tk " + total
                + "   (price rose by each optional add-on above)");
        System.out.println("---------------------------------------------\n");
    }

    private boolean printGroup(boolean base) {
        boolean printed = false;
        for (LineItem it : items) {
            if (it.isBase == base) {
                System.out.printf("      %-12s x%d @ Tk %-3d = Tk %d%n",
                        it.label, it.qty, it.unitPrice, it.subtotal());
                printed = true;
            }
        }
        return printed;
    }
}

// ---------------- The Builder ------------------------------------------------
class BurgerBuilder {
    // Prices in one place -> change once, applies everywhere.
    private static final int BUN = 20, PATTY = 80, CHEESE = 30, BBQ = 20, SALAD = 10;

    private int cheese, bbq, salad, extraPatty;   // repeatable add-on counts

    // fluent, repeatable optional steps
    BurgerBuilder addCheese() { cheese++;     return this; }
    BurgerBuilder addBbq()    { bbq++;        return this; }
    BurgerBuilder addSalad()  { salad++;      return this; }
    BurgerBuilder addPatty()  { extraPatty++; return this; }

    Burger build() {
        List<LineItem> items = new ArrayList<>();
        // mandatory base
        items.add(base("Bun", 2, BUN));
        items.add(base("Patty", 1, PATTY));
        // optional add-ons (only if chosen)
        if (extraPatty > 0) items.add(added("Extra Patty", extraPatty, PATTY));
        if (cheese > 0)     items.add(added("Cheese", cheese, CHEESE));
        if (bbq > 0)        items.add(added("Bbq Sauce", bbq, BBQ));
        if (salad > 0)      items.add(added("Salad", salad, SALAD));
        return new Burger(items);
    }

    private LineItem base(String l, int q, int p)  { LineItem i = new LineItem(l, q, p); i.isBase = true;  return i; }
    private LineItem added(String l, int q, int p) { LineItem i = new LineItem(l, q, p); i.isBase = false; return i; }
}

public class BurgerBuilderDemo {
    public static void main(String[] args) {
        // Test case 1: base only.
        new BurgerBuilder().build().printOrder();

        // Test case 2: double cheese, bbq, one extra patty (add-ons repeated).
        new BurgerBuilder()
                .addCheese().addCheese()
                .addBbq()
                .addPatty()
                .build()
                .printOrder();

        // Test case 3: the loaded burger.
        new BurgerBuilder()
                .addPatty().addPatty()
                .addCheese().addCheese().addCheese()
                .addBbq()
                .addSalad().addSalad()
                .build()
                .printOrder();
    }
}
