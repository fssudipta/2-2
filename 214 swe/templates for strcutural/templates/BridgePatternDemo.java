// ==================== 1. IMPLEMENTOR INTERFACE ====================
// Defines the implementation side (the "how")
interface Implementor {
    void operationImpl();
    // Add more implementation-specific methods as needed
}

// ==================== 2. CONCRETE IMPLEMENTORS ====================
// Provide actual implementations
class ConcreteImplementorA implements Implementor {
    @Override
    public void operationImpl() {
        System.out.println("ConcreteImplementorA: executing...");
        // Actual implementation logic here
    }
}

class ConcreteImplementorB implements Implementor {
    @Override
    public void operationImpl() {
        System.out.println("ConcreteImplementorB: executing...");
        // Actual implementation logic here
    }
}

// ==================== 3. ABSTRACTION ====================
// Defines the abstraction side (the "what")
// Holds a reference to Implementor (THE BRIDGE)
abstract class Abstraction {
    protected Implementor implementor;  // ← THE BRIDGE
    
    public Abstraction(Implementor implementor) {
        this.implementor = implementor;
    }
    
    // Optional: allow changing implementation at runtime
    public void setImplementor(Implementor implementor) {
        this.implementor = implementor;
    }
    
    // Abstraction operation that delegates to implementation
    public abstract void operation();
}

// ==================== 4. REFINED ABSTRACTIONS ====================
// Extend abstraction with additional behavior
class RefinedAbstractionA extends Abstraction {
    public RefinedAbstractionA(Implementor implementor) {
        super(implementor);
    }
    
    @Override
    public void operation() {
        System.out.println("RefinedAbstractionA: before");
        implementor.operationImpl();  // ← Delegate via bridge
        System.out.println("RefinedAbstractionA: after");
    }
}

class RefinedAbstractionB extends Abstraction {
    public RefinedAbstractionB(Implementor implementor) {
        super(implementor);
    }
    
    @Override
    public void operation() {
        System.out.println("RefinedAbstractionB: processing");
        implementor.operationImpl();  // ← Delegate via bridge
    }
}

// ==================== 5. CLIENT USAGE ====================
public class BridgePatternDemo {
    public static void main(String[] args) {
        // Create implementation
        Implementor implA = new ConcreteImplementorA();
        Implementor implB = new ConcreteImplementorB();
        
        // Create abstraction with implementation (BUILD THE BRIDGE)
        Abstraction abs1 = new RefinedAbstractionA(implA);
        Abstraction abs2 = new RefinedAbstractionB(implB);
        
        // Use them
        abs1.operation();
        abs2.operation();
        
        // 🔄 Swap implementation at runtime (Bridge flexibility!)
        abs1.setImplementor(implB);
        abs1.operation();  // Now uses ConcreteImplementorB
    }
}