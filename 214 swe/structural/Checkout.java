public class Checkout {
    // public double processPurchase(PurchaseableItem item) {
    // if (item == null)
    // throw new IllegalArgumentException("Cannot process null.");
    // return item.calculatePrice();
    // }

    public String generateReceipt(PurchaseableItem item) {
        if (item == null)
            throw new IllegalArgumentException("Cannot generate receipt for null item");

        StringBuilder receipt = new StringBuilder();
        receipt.append("=".repeat(60)).append("\n");
        receipt.append("                    EDULEARN PLATFORM\n");
        receipt.append("                       RECEIPT\n");
        receipt.append("=".repeat(60)).append("\n\n");
        receipt.append(item.getDetails(0)).append("\n\n");
        receipt.append("=".repeat(60)).append("\n");
        receipt.append(String.format("TOTAL DURATION: %.2f hours%n", item.getDuration()));
        receipt.append(String.format("TOTAL AMOUNT: $%.2f%n", item.calculatePrice()));
        receipt.append("=".repeat(60)).append("\n");
        receipt.append("\nThank you for your purchase!\n");

        return receipt.toString();
    }

    public boolean validatePurchase(PurchaseableItem item) {
        if (item == null)
            return false;
        if (item.calculatePrice() < 0)
            return false;
        if (item.getDuration() < 0)
            return false;
        return true;
    }

    public String processAndGenerateReceipt(PurchaseableItem item) {
        if (!validatePurchase(item))
            throw new IllegalStateException("Invalid purchase item");
        // double price = processPurchase(item);
        return generateReceipt(item);
    }
}
