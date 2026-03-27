import java.util.*;

interface Widget {
    void onUpdate(String stock, double price);
}

class TickerTape implements Widget {
    public void onUpdate(String s, double p) {
        System.out.println("[Ticker] Scrolling: " + s + " = $" + p);
    }
}

class Graph implements Widget {
    public void onUpdate(String s, double p) {
        System.out.println("[Graph] Plotting: " + s + " @ $" + p);
    }
}

class BuySellBot implements Widget {
    public void onUpdate(String s, double p) {
        System.out.println("[Bot] " + s + " @ $" + p + " -> " + (p > 1550 ? "SELL" : "BUY"));
    }
}

class StockFeed {
    String name;
    double price;
    List<Widget> widgets = new ArrayList<>();

    StockFeed(String n, double p) {
        name = n;
        price = p;
    }

    void add(Widget w) {
        widgets.add(w);
    }

    void remove(Widget w) {
        widgets.remove(w);
    }

    void setPrice(double p) {
        price = p;
        System.out.println("\n[" + name + "] Price -> $" + p);
        for (Widget w : widgets)
            w.onUpdate(name, p);
    }
}

public class C2_Stock {
    public static void main(String[] args) {
        StockFeed google = new StockFeed("GOOGL", 1500);
        Widget ticker = new TickerTape(), graph = new Graph(), bot = new BuySellBot();

        google.add(ticker);
        google.add(graph);
        google.add(bot);
        google.setPrice(1560);

        google.remove(bot);
        System.out.println("[Bot removed]");
        google.setPrice(1490);
    }
}