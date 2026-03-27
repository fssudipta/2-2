import java.util.*;

interface Observer {
    void update(String stock, double price);
}

class User implements Observer {
    String name;

    User(String n) {
        name = n;
    }

    public void update(String stock, double price) {
        System.out.println("  " + name + " notified: " + stock + " = " + price);
    }
}

class Stock {
    String name;
    double price;
    List<Observer> users = new ArrayList<>();

    Stock(String n, double p) {
        name = n;
        price = p;
    }

    void follow(Observer o) {
        users.add(o);
    }

    void unfollow(Observer o) {
        users.remove(o);
    }

    void setPrice(double p) {
        price = p;
        for (Observer o : users)
            o.update(name, p);
    }
}

public class Sec_C {
    public static void main(String[] args) {
        Stock google = new Stock("Google", 1500);
        Stock apple = new Stock("Apple", 1200);
        User alice = new User("Alice"), bob = new User("Bob");

        google.follow(alice);
        google.follow(bob);
        apple.follow(alice);

        System.out.println("Updating Google stock price...");
        google.setPrice(1550);
        System.out.println("\nUpdating Apple stock price...");
        apple.setPrice(1250);

        google.unfollow(alice);
        System.out.println("\nUpdating Google stock price again...");
        google.setPrice(1600);
    }
}