interface Payment {
    void pay(double amount);
}

class CreditCard implements Payment {
    public void pay(double amt) {
        System.out.println("[CreditCard] Charged $" + amt);
    }
}

class Bkash implements Payment {
    public void pay(double amt) {
        System.out.println("[bKash] Sent $" + amt);
    }
}

class Bitcoin implements Payment {
    public void pay(double amt) {
        System.out.println("[Bitcoin] Transferred $" + amt);
    }
}

class Checkout {
    Payment method;

    void setMethod(Payment p) {
        method = p;
    }

    void pay(double amt) {
        method.pay(amt);
    }
}

public class Sec_A {
    public static void main(String[] args) {
        Checkout c = new Checkout();
        c.setMethod(new CreditCard());
        c.pay(250);
        c.setMethod(new Bkash());
        c.pay(150);
        c.setMethod(new Bitcoin());
        c.pay(500);
    }
}