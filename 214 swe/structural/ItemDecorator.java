public abstract class ItemDecorator implements PurchaseableItem{
    protected PurchaseableItem wrappedItem;
    public ItemDecorator(PurchaseableItem item){
        if(item==null) throw new IllegalArgumentException("Item to decorate can't be null.");
        this.wrappedItem=item;
    }
    @Override
    public double calculatePrice(){
        return wrappedItem.calculatePrice();
    }
    @Override
    public double getDuration(){
        return wrappedItem.getDuration();
    }
    @Override
    public String getName(){
        return wrappedItem.getName();
    }
    @Override
    public String getDetails(int indent){
        return wrappedItem.getDetails(indent);
    }
}
