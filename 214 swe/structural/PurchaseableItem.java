public interface PurchaseableItem {
    double calculatePrice();
    double getDuration();
    String getName();
    String getDetails(int indent);
}
