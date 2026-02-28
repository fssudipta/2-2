import java.util.*;
// ==================== 1. COMPONENT INTERFACE ====================
interface Component {
    void operation();
    // Optional: common methods for both leaf and composite
    default void add(Component c) { throw new UnsupportedOperationException(); }
    default void remove(Component c) { throw new UnsupportedOperationException(); }
    default Component getChild(int i) { throw new UnsupportedOperationException(); }
}

// ==================== 2. LEAF (no children) ====================
class Leaf implements Component {
    private String name;
    
    public Leaf(String name) {
        this.name = name;
    }
    
    @Override
    public void operation() {
        System.out.println("Leaf: " + name);
    }
}

// ==================== 3. COMPOSITE (has children) ====================
class Composite implements Component {
    private String name;
    private List<Component> children = new ArrayList<>();
    
    public Composite(String name) {
        this.name = name;
    }
    
    @Override
    public void add(Component c) {
        children.add(c);
    }
    
    @Override
    public void remove(Component c) {
        children.remove(c);
    }
    
    @Override
    public Component getChild(int i) {
        return children.get(i);
    }
    
    @Override
    public void operation() {
        System.out.println("Composite: " + name);
        // Recursively call operation on children
        for (Component child : children) {
            child.operation();
        }
    }
}

// ==================== 4. CLIENT USAGE ====================
public class CompositeDemo {
    public static void main(String[] args) {
        // Create leaf nodes
        Leaf leaf1 = new Leaf("Leaf A");
        Leaf leaf2 = new Leaf("Leaf B");
        
        // Create composite nodes
        Composite subTree = new Composite("Sub-Tree");
        subTree.add(leaf1);
        subTree.add(leaf2);
        
        Composite root = new Composite("Root");
        root.add(subTree);
        root.add(new Leaf("Leaf C"));
        
        // Uniform treatment: call operation on any component
        root.operation();  // Recursively prints entire tree
    }
}