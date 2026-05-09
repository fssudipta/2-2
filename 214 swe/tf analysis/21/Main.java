enum CustomerType { REGULAR, PREMIUM }
enum ProductType { ELECTRONICS, GROCERY }

// Represents the "Data Clump" of customer info
class Customer {
    private final String id;
    private final String name;
    private final CustomerType type;

    public Customer(String id, String name, CustomerType type) {
        this.id = id;
        this.name = name;
        this.type = type;
    }

    public void printInfo() {
        System.out.println("Customer Name: " + name);
        System.out.println("Customer ID: " + id);
        System.out.println("Customer Type: " + type);
    }

    public CustomerType getType() { return type; }
}

interface DiscountStrategy {
    double getDiscountRate(ProductType product);
}

class RegularDiscount implements DiscountStrategy {
    public double getDiscountRate(ProductType product) {
        return (product == ProductType.ELECTRONICS) ? 0.10 : 0.05;
    }
}

class PremiumDiscount implements DiscountStrategy {
    public double getDiscountRate(ProductType product) {
        return (product == ProductType.ELECTRONICS) ? 0.20 : 0.10;
    }
}

class DiscountCalculator {
    // Fixes Feature Envy: Calculator no longer prints customer info
    public double calculateDiscount(Customer customer, ProductType product, double price) {
        DiscountStrategy strategy;
        
        // Strategy selection logic
        if (customer.getType() == CustomerType.PREMIUM) {
            strategy = new PremiumDiscount();
        } else {
            strategy = new RegularDiscount();
        }
        
        double rate = strategy.getDiscountRate(product);
        return price * rate;
    }
}

class OrderProcessor {
    private final DiscountCalculator discountCalculator = new DiscountCalculator();

    public void processOrder(Customer customer, ProductType product, double price) {
        System.out.println("--- Processing Order ---");
        customer.printInfo(); // Delegated printing to the owner of the data

        double discount = discountCalculator.calculateDiscount(customer, product, price);
        double finalPrice = price - discount;

        System.out.println("Product Type: " + product);
        System.out.println("Original Price: $" + price);
        
        if (discount > 0) {
            System.out.println("Discount Applied: $" + discount);
        } else {
            System.out.println("No discount applied.");
        }
        
        System.out.println("Final Price: $" + finalPrice);
    }
}

public class Main {
    public static void main(String[] args) {
        OrderProcessor processor = new OrderProcessor();

        // Example 1: Regular Customer buying Electronics
        Customer user1 = new Customer("C001", "Alice", CustomerType.REGULAR);
        processor.processOrder(user1, ProductType.ELECTRONICS, 1000.0);

        System.out.println();

        // Example 2: Premium Customer buying Groceries
        Customer user2 = new Customer("C002", "Bob", CustomerType.PREMIUM);
        processor.processOrder(user2, ProductType.GROCERY, 200.0);
    }
}