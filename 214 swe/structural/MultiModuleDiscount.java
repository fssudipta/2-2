public class MultiModuleDiscount extends ItemDecorator {
    private static final double DISCOUNT_AMOUNT = 15.0;
    private int moduleCount;

    public MultiModuleDiscount(PurchaseableItem item, int moduleCount) {
        super(item);
        if (moduleCount < 0)
            throw new IllegalArgumentException("Module count can't be negative.");
        this.moduleCount = moduleCount;
    }

    @Override
    public double calculatePrice() {
        double basePrice = wrappedItem.calculatePrice();
        if (moduleCount >= 2)
            return Math.max(0, basePrice - DISCOUNT_AMOUNT);
        return basePrice;
    }

    @Override
    public String getDetails(int indent) {
        String baseDetails = wrappedItem.getDetails(indent);
        String indentation = "  ".repeat(indent);

        if (moduleCount >= 2) {
            return baseDetails + "\n" +
                    String.format("%s[Discount] Multi-Module Discount (%d modules): -$%.2f",
                            indentation, moduleCount, DISCOUNT_AMOUNT);
        }
        return baseDetails;
    }

    @Override
    public String toString() {
        return getDetails(0);
    }
}
