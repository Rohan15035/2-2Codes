// ============================================================================
// Q5  (CSE 214 - C1)  E-commerce payments
// Payment methods: Credit card, PayPal, Bitcoin. New methods must be addable and
// old ones changeable WITHOUT modifying existing code. The user picks a method
// and pays; a success message is shown.
//
// PATTERN : FACTORY METHOD  (via a self-registering Simple Factory)
//   PaymentMethod is the product interface. Each concrete method registers its
//   own creator with PaymentFactory. PaymentFactory.create(name) returns the
//   right object. Because the factory looks methods up in a registry (not a
//   hard-coded switch), adding a new method never edits the factory or client.
//
// SOLID (the point the question is really testing):
//   - OCP : "accommodate changes without modifying the existing codebase" ->
//           add a new class + one register() call; the factory/client stay put.
//   - DIP : the checkout code depends on the PaymentMethod abstraction only.
//   - LSP : every method is usable wherever a PaymentMethod is expected.
//   - SRP : each class knows how to process exactly one kind of payment.
// ============================================================================

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Supplier;

// ---------------- Product interface ------------------------------------------
interface PaymentMethod {
    String name();
    void processPayment(double amount);
}

// ---------------- Concrete payment methods -----------------------------------
class CreditCardPayment implements PaymentMethod {
    public String name() { return "Credit Card"; }
    public void processPayment(double amount) {
        System.out.printf("[Credit Card] Authorising Tk %.2f via card network...%n", amount);
        System.out.println("Payment successful with Credit Card.");
    }
}

class PayPalPayment implements PaymentMethod {
    public String name() { return "PayPal"; }
    public void processPayment(double amount) {
        System.out.printf("[PayPal] Redirecting to PayPal for Tk %.2f...%n", amount);
        System.out.println("Payment successful with PayPal.");
    }
}

class BitcoinPayment implements PaymentMethod {
    public String name() { return "Bitcoin"; }
    public void processPayment(double amount) {
        System.out.printf("[Bitcoin] Broadcasting transaction for Tk %.2f...%n", amount);
        System.out.println("Payment successful with Bitcoin.");
    }
}

// ---------------- The factory (registry-based -> Open/Closed) ----------------
class PaymentFactory {
    private static final Map<String, Supplier<PaymentMethod>> registry = new LinkedHashMap<>();

    // New methods plug in here; the factory code never changes.
    static void register(String key, Supplier<PaymentMethod> creator) {
        registry.put(key.toLowerCase(), creator);
    }

    static PaymentMethod create(String key) {
        Supplier<PaymentMethod> creator = registry.get(key.toLowerCase());
        if (creator == null) throw new IllegalArgumentException("Unsupported payment method: " + key);
        return creator.get();
    }

    static void printAvailable() {
        System.out.println("Available methods: " + registry.keySet());
    }
}

public class PaymentSystemDemo {

    // Register the built-in methods once at startup.
    static {
        PaymentFactory.register("card",    CreditCardPayment::new);
        PaymentFactory.register("paypal",  PayPalPayment::new);
        PaymentFactory.register("bitcoin", BitcoinPayment::new);
    }

    // The checkout code depends only on the abstraction.
    static void checkout(String chosenMethod, double amount) {
        System.out.println("--- User chose: " + chosenMethod + " ---");
        try {
            PaymentMethod method = PaymentFactory.create(chosenMethod);
            method.processPayment(amount);
        } catch (IllegalArgumentException ex) {
            System.out.println("  [Rejected] " + ex.getMessage());
        }
        System.out.println();
    }

    public static void main(String[] args) {
        PaymentFactory.printAvailable();
        System.out.println();

        checkout("card", 1500);
        checkout("paypal", 2999.99);
        checkout("bitcoin", 500);
        checkout("cash", 100);   // boundary: unsupported method

        // ---- Demonstrating OCP: a brand-new method added with ZERO edits above.
        System.out.println(">> Business adds a new method later (no existing code touched):");
        PaymentFactory.register("gpay", () -> new PaymentMethod() {
            public String name() { return "Google Pay"; }
            public void processPayment(double amount) {
                System.out.printf("[Google Pay] Charging Tk %.2f...%n", amount);
                System.out.println("Payment successful with Google Pay.");
            }
        });
        checkout("gpay", 750);
    }
}
