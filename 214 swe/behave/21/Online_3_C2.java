interface OrderState {
    void next(Order o);

    void cancel(Order o);

    String status();
}

class Placed implements OrderState {
    public void next(Order o) {
        System.out.println("-> Confirmed");
        o.state = new Confirmed();
    }

    public void cancel(Order o) {
        System.out.println("-> Cancelled");
        o.state = new Cancelled();
    }

    public String status() {
        return "Placed";
    }
}

class Confirmed implements OrderState {
    public void next(Order o) {
        System.out.println("-> Shipped");
        o.state = new Shipped();
    }

    public void cancel(Order o) {
        System.out.println("-> Cancelled");
        o.state = new Cancelled();
    }

    public String status() {
        return "Confirmed";
    }
}

class Shipped implements OrderState {
    public void next(Order o) {
        System.out.println("-> Delivered");
        o.state = new Delivered();
    }

    public void cancel(Order o) {
        System.out.println("Cannot cancel — already shipped!");
    }

    public String status() {
        return "Shipped";
    }
}

class Delivered implements OrderState {
    public void next(Order o) {
        System.out.println("Already delivered.");
    }

    public void cancel(Order o) {
        System.out.println("Cannot cancel — already delivered!");
    }

    public String status() {
        return "Delivered";
    }
}

class Cancelled implements OrderState {
    public void next(Order o) {
        System.out.println("Order is cancelled.");
    }

    public void cancel(Order o) {
        System.out.println("Already cancelled.");
    }

    public String status() {
        return "Cancelled";
    }
}

class Order {
    OrderState state = new Placed();
    String id;

    Order(String id) {
        this.id = id;
        System.out.println("Order " + id + " -> " + state.status());
    }

    void next() {
        state.next(this);
        System.out.println("  Status: " + state.status());
    }

    void cancel() {
        state.cancel(this);
        System.out.println("  Status: " + state.status());
    }
}

public class Online_3_C2 {
    public static void main(String[] args) {
        Order o1 = new Order("ORD-001");
        o1.next();
        o1.next();
        o1.cancel();
        o1.next(); // ship, can't cancel, deliver

        System.out.println();
        Order o2 = new Order("ORD-002");
        o2.next();
        o2.cancel();
        o2.next(); // confirm, cancel, can't proceed
    }
}