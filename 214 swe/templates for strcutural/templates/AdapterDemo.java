// ==================== 1. TARGET INTERFACE ====================
// What the client expects
interface Target {
    void request();
}

// ==================== 2. ADAPTEE ====================
// The existing class with incompatible interface
class Adaptee {
    public void specificRequest() {
        System.out.println("Adaptee: specific behavior");
    }
}

// ==================== 3. ADAPTER (Object Adapter - Recommended) ====================
class Adapter implements Target {
    private Adaptee adaptee;  // ← Holds reference to adaptee
    
    public Adapter(Adaptee adaptee) {
        this.adaptee = adaptee;
    }
    
    @Override
    public void request() {
        // Translate Target request to Adaptee request
        System.out.println("Adapter: translating request");
        adaptee.specificRequest();  // ← Call adaptee method
    }
}

// ==================== ALTERNATIVE: Class Adapter (Inheritance) ====================
// Only use if you can extend Adaptee (less flexible)
/*
class ClassAdapter extends Adaptee implements Target {
    @Override
    public void request() {
        specificRequest();  // Direct call via inheritance
    }
}
*/

// ==================== 4. CLIENT USAGE ====================
public class AdapterDemo {
    public static void main(String[] args) {
        // Client has Target interface
        Target target = new Adapter(new Adaptee());
        
        // Client uses Target interface, Adapter translates to Adaptee
        target.request();
    }
}