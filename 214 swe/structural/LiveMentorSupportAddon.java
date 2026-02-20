public class LiveMentorSupportAddon extends ItemDecorator {
    private static final double MENTOR_SUPPORT_PRICE = 20.0;

    public LiveMentorSupportAddon(PurchaseableItem item) {
        super(item);
    }

    @Override
    public double calculatePrice() {
        return wrappedItem.calculatePrice() + MENTOR_SUPPORT_PRICE;
    }

    @Override
    public String getDetails(int indent) {
        String baseDetails = wrappedItem.getDetails(indent);
        String indentation = "  ".repeat(indent);
        return baseDetails + "\n"
                + String.format("%s[Add-on] Live Mentor Support: $%.2f", indentation, MENTOR_SUPPORT_PRICE);
    }

    @Override
    public String toString() {
        return getDetails(0);
    }
}
