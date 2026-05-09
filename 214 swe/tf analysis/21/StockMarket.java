import java.util.ArrayList;
import java.util.List;

interface StockExchange {
    public void register(StockObserver newObserver);

    public void unregister(StockObserver newObserver);

    public void notifyAllObserver(String company, double price);
}

interface Observer {
    public void update(String company, double price);
}

class StockObserver implements Observer {

    private int observerID;
    private String observerName;
    private double aplPrice;
    private double googPrice;
    private double ibmPrice;
    private StockGrabber stockGrabber;

    public StockObserver(StockGrabber stockGrabber, String name) {
        this.stockGrabber = stockGrabber;
        this.observerName = name;
        this.observerID = StockGrabber.getNextId(); // auto-generated starting from 1
        stockGrabber.register(this);

        // On registration, immediately knows all current prices
        this.aplPrice = stockGrabber.getAplPrice();
        this.googPrice = stockGrabber.getGoogPrice();
        this.ibmPrice = stockGrabber.getIbmPrice();

        printPrices();
    }

    @Override
    public void update(String company, double price) {
        if (company.equals("APL"))
            this.aplPrice = price;
        else if (company.equals("GOOG"))
            this.googPrice = price;
        else if (company.equals("IBM"))
            this.ibmPrice = price;
        printPrices();
    }

    private void printPrices() {
        System.out.println("Observer " + observerID + " (" + observerName + "):");
        System.out.println("  APL:  $" + aplPrice);
        System.out.println("  GOOG: $" + googPrice);
        System.out.println("  IBM:  $" + ibmPrice);
    }
}

class StockGrabber implements StockExchange {

    private List<StockObserver> observers = new ArrayList<>();
    private double aplPrice = 230.0;
    private double googPrice = 200.0;
    private double ibmPrice = 180.0;
    private static int observerCount = 1;
    private String name;

    public StockGrabber(String name) {
        this.name = name;
    }

    public static int getNextId() {
        return observerCount++;
    }

    @Override
    public void register(StockObserver newObserver) {
        observers.add(newObserver);
    }

    @Override
    public void unregister(StockObserver newObserver) {
        observers.remove(newObserver);
    }

    @Override
    public void notifyAllObserver(String company, double price) {
        for (StockObserver observer : observers) {
            observer.update(company, price);
        }
    }

    public void setAplPrice(double price) {
        if (this.aplPrice != price) {
            this.aplPrice = price;
            notifyAllObserver("APL", price);
        }
    }

    public void setGoogPrice(double price) {
        if (this.googPrice != price) {
            this.googPrice = price;
            notifyAllObserver("GOOG", price);
        }
    }

    public void setIbmPrice(double price) {
        if (this.ibmPrice != price) {
            this.ibmPrice = price;
            notifyAllObserver("IBM", price);
        }
    }

    public double getAplPrice() {
        return aplPrice;
    }

    public double getGoogPrice() {
        return googPrice;
    }

    public double getIbmPrice() {
        return ibmPrice;
    }
}

public class StockMarket {
    public static void main(String[] args) {
        StockGrabber sc = new StockGrabber("shamol");
        Observer o1 = new StockObserver(sc, "gadha");
        Observer o2 = new StockObserver(sc, "goru");
        sc.setAplPrice(250.0);
        sc.setGoogPrice(200.0);
    }
}