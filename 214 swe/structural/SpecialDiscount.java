public class SpecialDiscount extends ItemDecorator {
    private static final double DISCOUNT_AMOUNT = 12.0;
    private static final double MINIMUM_DURATION = 5.0;

    public SpecialDiscount(PurchaseableItem item) {
        super(item);
    }

    @Override
    public double calculatePrice() {
        double basePrice = wrappedItem.calculatePrice();
        double duration = wrappedItem.getDuration();
        if (duration >= MINIMUM_DURATION)
            return Math.max(0, basePrice - DISCOUNT_AMOUNT);
        return basePrice;
    }

    @Override
    public String getDetails(int indent) {
        String baseDetails = wrappedItem.getDetails(indent);
        String indentation = "  ".repeat(indent);
        double duration = wrappedItem.getDuration();

        if (duration >= MINIMUM_DURATION) {
            return baseDetails + "\n" +
                    String.format("%s[Discount] Special Discount (%.2f hrs >= %.2f hrs): -$%.2f",
                            indentation, duration, MINIMUM_DURATION, DISCOUNT_AMOUNT);
        }
        return baseDetails;
    }

    @Override
    public String toString() {
        return getDetails(0);
    }
}
