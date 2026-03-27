// 1. The Strategy Interface
interface RouteStrategy { void buildRoute(String start, String end); }

// 2. Concrete Strategies
class RoadStrategy implements RouteStrategy {
    public void buildRoute(String s, String e) { System.out.println("Driving from " + s + " to " + e); }
}

class WalkingStrategy implements RouteStrategy {
    public void buildRoute(String s, String e) { System.out.println("Walking from " + s + " to " + e); }
}

// 3. The Context (The object that uses the strategy)
class Navigator {
    private RouteStrategy strategy; // Reference to the interface
    public void setStrategy(RouteStrategy s) { this.strategy = s; }
    public void navigate(String s, String e) { strategy.buildRoute(s, e); }
}

// 4. The Client (Main)
public class StrategyMain {
    public static void main(String[] args) {
        Navigator nav = new Navigator();
        
        // Client decides which strategy to "inject"
        nav.setStrategy(new RoadStrategy());
        nav.navigate("Home", "Office");
        
        nav.setStrategy(new WalkingStrategy());
        nav.navigate("Office", "Park");
    }
}