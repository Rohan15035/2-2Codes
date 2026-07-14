
// class Logger {

//     Logger instance;

//     private Logger() {

//     }

//     public void useLogger() {
//         instance = new Logger();
//     }

//     public void deposit() {
//         System.out.println("Deposit");

//     }

//     public void withdrawal() {
//         System.out.println("withdrawal");
//     }

//     public void transfer() {
//         System.out.println("transfer");
//     }

// };

interface Notification {
    public void notifyUser();
}

class SMS implements Notification {

    @Override
    public void notifyUser() {
        System.out.println("SMS");
    }
}

class Email implements Notification {
    @Override
    public void notifyUser() {
        System.out.println("Email");
    }
}

class PushNotiification implements Notification {
    @Override
    public void notifyUser() {
        System.out.println("Push Notificaiton");
    }
}

class handler {

    public Notification generate(String s) {

    }

}

public class demo {

}

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
