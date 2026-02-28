
// Step 1: Define the base Purchase component interface
interface Purchase {
    double calculatePrice();
}

class BasePurchase implements Purchase {

    private double basePrice;

    public BasePurchase(double basePrice) {
        this.basePrice = basePrice;
    }

    public double calculatePrice() {
        return basePrice;
    }
}

abstract class PurchaseDecorator implements Purchase {

    protected Purchase purchase;

    public PurchaseDecorator(Purchase purchase) {
        this.purchase = purchase;
    }
}


class LoyaltyDiscount extends PurchaseDecorator {

    public LoyaltyDiscount(Purchase purchase) {
        super(purchase);
    }

    public double calculatePrice() {
        double price = purchase.calculatePrice();
        return price * 0.90;
    }
}


class SeasonalDiscount extends PurchaseDecorator {

    public SeasonalDiscount(Purchase purchase) {
        super(purchase);
    }

    public double calculatePrice() {
        return purchase.calculatePrice() - 100;
    }
}


class HighValueDiscount extends PurchaseDecorator {

    public HighValueDiscount(Purchase purchase) {
        super(purchase);
    }

    public double calculatePrice() {
        double price = purchase.calculatePrice();
        if (price > 10000) {
            price = price * 0.98;
        }
        return price;
    }
}


public class online_secB1 {

    public static void main(String[] args) {

        double basePrice = 12000;

        // Step 1: Base purchase
        Purchase purchase = new BasePurchase(basePrice);

        // Step 2: Apply discounts conditionally
        Purchase discountedPurchase = purchase;

        boolean isPremiumMember = true;
        boolean isSeasonalOffer = true;

        if (isPremiumMember) {
            discountedPurchase =
                new LoyaltyDiscount(discountedPurchase);
        }

        if (isSeasonalOffer) {
            discountedPurchase =
                new SeasonalDiscount(discountedPurchase);
        }

        discountedPurchase =
            new HighValueDiscount(discountedPurchase);

        // Step 3: Final price
        double finalPrice =
                discountedPurchase.calculatePrice();

        System.out.println(
            "Final price after all discounts: " + finalPrice);
    }
}

