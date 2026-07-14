// ===================================================================
// B2 : Cross-platform notification library  ->  FACTORY PATTERN
// -------------------------------------------------------------------
// The client passes a channel string ("SMS"/"Email"/"Push") and gets
// back a Notification through the interface only - it never names the
// concrete classes.
//
// Instead of a switch/if-else that must be EDITED for every new type,
// the factory keeps a REGISTRY (Map: channel -> constructor). This
// honours the Open/Closed Principle: adding "SlackMessage" later is
// 1 new class + 1 register() line, and the dispatch code below never
// changes. No case, no if-else chain.
// ===================================================================

import java.util.Map;
import java.util.HashMap;
import java.util.Objects;
import java.util.Optional;
import java.util.function.Supplier;

// Common product interface
interface Notification {
    void notifyUser();
}

// Concrete products
class SMSNotification implements Notification {
    public void notifyUser() {
        System.out.println("Sending an SMS notification.");
    }
}

class EmailNotification implements Notification {
    public void notifyUser() {
        System.out.println("Sending an Email notification.");
    }
}

class PushNotification implements Notification {
    public void notifyUser() {
        System.out.println("Sending a Push notification.");
    }
}

// The Factory: a registry maps a channel string -> a way to build the object.
// Supplier<Notification> holds a constructor reference (e.g.
// SMSNotification::new).
class NotificationFactory {

    private static final Map<String, Supplier<Notification>> registry = new HashMap<>();

    // Register the built-in channels once, when the class loads.
    static {
        register("sms", SMSNotification::new);
        register("email", EmailNotification::new);
        register("push", PushNotification::new);
        // Future: register("slack", SlackMessage::new); <-- the ONLY line you add
    }

    // Extension point: new types plug in here (case-insensitive keys).
    public static void register(String channel, Supplier<Notification> constructor) {
        registry.put(channel.toLowerCase(), constructor);
    }

    // Dispatch with no switch and no if-else: look the key up, build, or fail.
    public static Notification create(String channel) {
        Objects.requireNonNull(channel, "Channel is required.");
        return Optional.ofNullable(registry.get(channel.toLowerCase()))
                .orElseThrow(() -> new IllegalArgumentException("Unknown channel: " + channel))
                .get();
    }
}

public class B2_NotificationFactory {
    public static void main(String[] args) {
        // Client only ever sees the Notification interface.
        Notification n = NotificationFactory.create("SMS");
        n.notifyUser();

        NotificationFactory.create("Email").notifyUser();
        NotificationFactory.create("Push").notifyUser();
    }
}

/////////////////
///
///
///
///
// ===================================================================
// B2 : Cross-platform notification library -> FACTORY PATTERN
// -------------------------------------------------------------------
// The client passes a channel string ("SMS"/"Email"/"Push") and gets
// back a Notification through the interface only - it never names the
// concrete classes. Adding "SlackMessage" later = 1 new class + 1 new
// line in the factory; the client code stays untouched.
// ===================================================================

// Common product interface
interface Notification {
    void notifyUser();
}

// Concrete products
class SMSNotification implements Notification {
    public void notifyUser() {
        System.out.println("Sending an SMS notification.");
    }
}

class EmailNotification implements Notification {
    public void notifyUser() {
        System.out.println("Sending an Email notification.");
    }
}

class PushNotification implements Notification {
    public void notifyUser() {
        System.out.println("Sending a Push notification.");
    }
}

// The Factory: single place that maps a string -> concrete object
class NotificationFactory {
    public static Notification create(String channel) {
        if (channel == null) {
            throw new IllegalArgumentException("Channel is required.");
        }
        switch (channel.toLowerCase()) {
            case "sms":
                return new SMSNotification();
            case "email":
                return new EmailNotification();
            case "push":
                return new PushNotification();
            // Future: case "slack": return new SlackMessage();
            default:
                throw new IllegalArgumentException("Unknown channel: " + channel);
        }
    }
}

public class B2_NotificationFactory {
    public static void main(String[] args) {
        // Client only ever sees the Notification interface.
        Notification n = NotificationFactory.create("SMS");
        n.notifyUser();

        NotificationFactory.create("Email").notifyUser();
        NotificationFactory.create("Push").notifyUser();
    }
}
