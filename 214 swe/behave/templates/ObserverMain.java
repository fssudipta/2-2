import java.util.*;

// 1. The Observer (Interface)
interface Subscriber { void update(String news); }

// 2. The Subject (The Publisher)
class NewsAgency {
    private List<Subscriber> subscribers = new ArrayList<>();
    public void subscribe(Subscriber s) { subscribers.add(s); }
    public void publish(String news) { 
        for(Subscriber s : subscribers) s.update(news); 
    }
}

// 3. Concrete Observer
class SmartphoneApp implements Subscriber {
    public void update(String news) { System.out.println("Phone Notification: " + news); }
}

// 4. The Client (Main)
public class ObserverMain {
    public static void main(String[] args) {
        NewsAgency bbc = new NewsAgency();
        SmartphoneApp user1 = new SmartphoneApp();
        
        bbc.subscribe(user1); // Client links Observer to Subject
        bbc.publish("Breaking: Java is still awesome.");
    }
}