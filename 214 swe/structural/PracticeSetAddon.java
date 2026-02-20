public class PracticeSetAddon extends ItemDecorator{
    private static final double PRACTICE_SET_PRICE=10.0;
    public PracticeSetAddon(PurchaseableItem item){
        super(item);
    }
    @Override
    public double calculatePrice(){
        return wrappedItem.calculatePrice()+PRACTICE_SET_PRICE;
    }
    @Override
    public String getDetails(int indent){
        String baseDetails=wrappedItem.getDetails(indent);
        String indentation=" ".repeat(indent);
        return baseDetails+"\n"+String.format("%s[Add-on] Practice Question Set: $%.2f", indentation, PRACTICE_SET_PRICE);
    }
    @Override
    public String toString(){
        return getDetails(0);
    }
}
