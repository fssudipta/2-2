public class DevelopingCountryDiscount extends ItemDecorator {
    private static final double DISCOUNT_AMOUNT=10.0;
    public DevelopingCountryDiscount(PurchaseableItem item){
        super(item);
    }
    @Override
    public double calculatePrice(){
        double basePrice=wrappedItem.calculatePrice();
        return Math.max(0, basePrice-DISCOUNT_AMOUNT);
    }
    @Override
    public String getDetails(int indent){
        String baseDetails=wrappedItem.getDetails(indent);
        String indentation=" ".repeat(indent);
        return baseDetails+"\n"+String.format("%s[Discount] Developing Country Student Discount: -$%.2f", indentation, DISCOUNT_AMOUNT);
    }
    @Override
    public String toString(){
        return getDetails(0);
    }
}
