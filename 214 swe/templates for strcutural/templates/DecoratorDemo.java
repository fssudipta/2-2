// ==================== 1. COMPONENT INTERFACE ====================
interface Component {
    void operation();
    // Add other methods as needed
}

// ==================== 2. CONCRETE COMPONENT ====================
class ConcreteComponent implements Component {
    @Override
    public void operation() {
        System.out.println("ConcreteComponent: base behavior");
    }
}

// ==================== 3. ABSTRACT DECORATOR ====================
abstract class Decorator implements Component {
    protected Component component;  // ← Holds reference to wrap
    
    public Decorator(Component component) {
        this.component = component;
    }
    
    @Override
    public void operation() {
        component.operation();  // ← Delegate to wrapped object
    }
}

// ==================== 4. CONCRETE DECORATORS ====================
class ConcreteDecoratorA extends Decorator {
    public ConcreteDecoratorA(Component component) {
        super(component);
    }
    
    @Override
    public void operation() {
        // Add behavior BEFORE
        super.operation();
        // Add behavior AFTER
        System.out.println("ConcreteDecoratorA: added behavior");
    }
}

class ConcreteDecoratorB extends Decorator {
    public ConcreteDecoratorB(Component component) {
        super(component);
    }
    
    @Override
    public void operation() {
        super.operation();
        System.out.println("ConcreteDecoratorB: added behavior");
    }
}

// ==================== 5. CLIENT USAGE ====================
public class DecoratorDemo {
    public static void main(String[] args) {
        // Start with base component
        Component component = new ConcreteComponent();
        
        // Wrap with decorators dynamically
        component = new ConcreteDecoratorA(component);
        component = new ConcreteDecoratorB(component);
        
        // Use the decorated object
        component.operation();
    }
}