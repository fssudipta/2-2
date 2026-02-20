public class Lesson implements PurchaseableItem {
    private String name;
    private double duration;
    private double price;

    public Lesson(String name, double duration, double price) {
        if (duration < 0)
            throw new IllegalArgumentException("Duration can't be negative.");
        if (price < 0)
            throw new IllegalArgumentException("Duration can't be negative.");
        this.name = name;
        this.price = price;
        this.duration = duration;
    }

    @Override
    public double calculatePrice() {
        return price;
    }

    @Override
    public double getDuration() {
        return duration;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public String getDetails(int indent) {
        String indentation = " ".repeat(indent);
        return String.format("%sLesson: %s (Duration: %.2f hrs, Price: $%.2f)", indentation, name, duration, price);
    }
}
