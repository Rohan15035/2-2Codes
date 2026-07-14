// ===================================================================
// B1 : Banking audit Logger  ->  SINGLETON PATTERN
// -------------------------------------------------------------------
// Only ONE Logger may exist so every module writes to the same single
// log file (no corruption / interleaving). Three ingredients:
//   1. private static field holding the sole instance
//   2. private constructor  -> nobody outside can call `new Logger()`
//   3. public static getInstance() -> the single global access point
// ===================================================================

class Logger {
    // 1. The one and only instance
    private static Logger instance;

    // 2. Private constructor blocks external instantiation
    private Logger() {
        System.out.println("Logger created: audit log file opened.");
    }

    // 3. Global access point (lazy initialization: created on first use)
    public static Logger getInstance() {
        if (instance == null) {
            instance = new Logger();
        }
        return instance;
    }

    public void log(String message) {
        System.out.println("[AUDIT LOG] " + message);
    }
}

// Two independent parts of the application that both need to log:
class DepositModule {
    void run() {
        Logger.getInstance().log("Deposit of $500 by Client A");
    }
}

class WithdrawModule {
    void run() {
        Logger.getInstance().log("Withdrawal of $200 by Client B");
    }
}

public class B1_Logger {
    public static void main(String[] args) {
        new DepositModule().run();
        new WithdrawModule().run();

        // Proof both clients share the SAME object:
        Logger a = Logger.getInstance();
        Logger b = Logger.getInstance();
        System.out.println("Same Logger instance? " + (a == b));
    }
}
