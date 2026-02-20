import java.util.ArrayList;
import java.util.List;

public class ShoppingCart implements PurchaseableItem {
    private List<PurchaseableItem> items;
    private String cartName;

    public ShoppingCart() {
        this("Shopping Cart");
    }

    public ShoppingCart(String cartName) {
        this.cartName = cartName;
        this.items = new ArrayList<>();
    }

    public void addItem(PurchaseableItem item) {
        if (item == null)
            throw new IllegalArgumentException("Item can't be null.");
        items.add(item);
    }

    public void removeItem(PurchaseableItem item) {
        items.remove(item);
    }

    public void clear() {
        items.clear();
    }

    public List<PurchaseableItem> getItems() {
        return new ArrayList<>(items);
    }

    public int getModuleCount() {
        int count = 0;
        for (PurchaseableItem item : items) {
            if (isModule(item))
                count++;
        }
        return count;
    }

    private boolean isModule(PurchaseableItem item) {
        PurchaseableItem current = item;
        while (current instanceof ItemDecorator) {
            current = ((ItemDecorator) current).wrappedItem;
        }
        return current instanceof Module;
    }

    public boolean isEmpty() {
        return items.isEmpty();
    }

    public int size() {
        return items.size();
    }

    @Override
    public double calculatePrice() {
        double total = 0;
        for (PurchaseableItem item : items)
            total += item.calculatePrice();
        return total;
    }

    @Override
    public double getDuration() {
        double total = 0;
        for (PurchaseableItem item : items)
            total += item.getDuration();
        return total;
    }

    @Override
    public String getName() {
        return cartName;
    }

    @Override
    public String getDetails(int indent) {
        String indentation = "  ".repeat(indent);
        StringBuilder sb = new StringBuilder();
        sb.append(String.format("%s=== %s ===%n", indentation, cartName));
        sb.append(String.format("%sTotal Items: %d%n", indentation, items.size()));
        sb.append(String.format("%sTotal Duration: %.2f hrs%n", indentation, getDuration()));
        sb.append(String.format("%sTotal Price: $%.2f%n%n", indentation, calculatePrice()));

        for (int i = 0; i < items.size(); i++) {
            sb.append(String.format("%sItem %d:%n", indentation, i + 1));
            sb.append(items.get(i).getDetails(indent + 1));
            if (i < items.size() - 1) {
                sb.append("\n\n");
            }
        }

        return sb.toString();
    }

    @Override
    public String toString() {
        return getDetails(0);
    }
}
