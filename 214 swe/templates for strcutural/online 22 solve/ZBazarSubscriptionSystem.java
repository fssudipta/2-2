import java.util.ArrayList;
import java.util.List;

// ==================== COMPONENT INTERFACE ====================
// Common interface for all packages and items
interface Package {
    String getName();
    double getPrice();
    double getWeight();
    void display(int indent);
}

// ==================== LEAF ====================
// Individual grocery items (cannot contain other items)
class GroceryItem implements Package {
    private String name;
    private double price;
    private double weight; // in kg
    
    public GroceryItem(String name, double price, double weight) {
        this.name = name;
        this.price = price;
        this.weight = weight;
    }
    
    @Override
    public String getName() {
        return name;
    }
    
    @Override
    public double getPrice() {
        return price;
    }
    
    @Override
    public double getWeight() {
        return weight;
    }
    
    @Override
    public void display(int indent) {
        System.out.println(getIndentString(indent) + 
                          "Item: " + name + 
                          " | Price: $" + String.format("%.2f", price) + 
                          " | Weight: " + weight + "kg");
    }
    
    private String getIndentString(int indent) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < indent; i++) {
            sb.append("  ");
        }
        return sb.toString();
    }
}

// ==================== COMPOSITE ====================
// Abstract base for packages that can contain other packages/items
abstract class BasePackage implements Package {
    protected String name;
    protected List<Package> packages = new ArrayList<>();
    
    public BasePackage(String name) {
        this.name = name;
    }
    
    public void addPackage(Package pkg) {
        packages.add(pkg);
    }
    
    public void removePackage(Package pkg) {
        packages.remove(pkg);
    }
    
    @Override
    public String getName() {
        return name;
    }
    
    @Override
    public double getPrice() {
        double total = 0;
        for (Package pkg : packages) {
            total += pkg.getPrice();
        }
        return total;
    }
    
    @Override
    public double getWeight() {
        double total = 0;
        for (Package pkg : packages) {
            total += pkg.getWeight();
        }
        return total;
    }
    
    @Override
    public void display(int indent) {
        System.out.println(getIndentString(indent) + 
                          "Package: " + name + 
                          " | Total Price: $" + String.format("%.2f", getPrice()) + 
                          " | Total Weight: " + String.format("%.2f", getWeight()) + "kg");
        
        for (Package pkg : packages) {
            pkg.display(indent + 1);
        }
    }
    
    private String getIndentString(int indent) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < indent; i++) {
            sb.append("  ");
        }
        return sb.toString();
    }
}

// ==================== CONCRETE COMPOSITES ====================

// Preset Package (Small, Family, Mega)
class PresetPackage extends BasePackage {
    public PresetPackage(String name) {
        super(name);
    }
    
    // Preset packages can only contain individual items (not other packages)
    public void addItem(GroceryItem item) {
        addPackage(item);
    }
}

// Custom Package (can contain items, preset packages, or other custom packages)
class CustomPackage extends BasePackage {
    public CustomPackage(String name) {
        super(name);
    }
    
    // Custom packages can contain anything
    public void addItem(GroceryItem item) {
        addPackage(item);
    }
    
    public void addPresetPackage(PresetPackage preset) {
        addPackage(preset);
    }
    
    public void addCustomPackage(CustomPackage custom) {
        addPackage(custom);
    }
}

// ==================== MAIN SYSTEM ====================
public class ZBazarSubscriptionSystem {
    
    public static void main(String[] args) {
        System.out.println("=== ZBazar Subscription-Based Grocery Delivery ===\n");
        
        // ==================== CREATE INDIVIDUAL ITEMS ====================
        GroceryItem rice = new GroceryItem("Rice", 15.0, 5.0);
        GroceryItem oil = new GroceryItem("Cooking Oil", 12.0, 2.0);
        GroceryItem pulse = new GroceryItem("Pulse", 8.0, 3.0);
        GroceryItem sugar = new GroceryItem("Sugar", 6.0, 2.0);
        GroceryItem flour = new GroceryItem("Flour", 10.0, 5.0);
        GroceryItem salt = new GroceryItem("Salt", 2.0, 1.0);
        GroceryItem tea = new GroceryItem("Tea", 5.0, 0.5);
        GroceryItem coffee = new GroceryItem("Coffee", 8.0, 0.5);
        GroceryItem spices = new GroceryItem("Spices Mix", 7.0, 0.8);
        GroceryItem pasta = new GroceryItem("Pasta", 4.0, 1.0);
        
        // ==================== CREATE PRESET PACKAGES ====================
        
        // Small Package
        PresetPackage smallPkg = new PresetPackage("Small Package");
        smallPkg.addItem(rice);
        smallPkg.addItem(oil);
        smallPkg.addItem(pulse);
        smallPkg.addItem(salt);
        
        // Family Package
        PresetPackage familyPkg = new PresetPackage("Family Package");
        familyPkg.addItem(rice);
        familyPkg.addItem(oil);
        familyPkg.addItem(pulse);
        familyPkg.addItem(sugar);
        familyPkg.addItem(flour);
        familyPkg.addItem(salt);
        familyPkg.addItem(tea);
        familyPkg.addItem(spices);
        
        // Mega Package
        PresetPackage megaPkg = new PresetPackage("Mega Package");
        megaPkg.addItem(rice);
        megaPkg.addItem(oil);
        megaPkg.addItem(pulse);
        megaPkg.addItem(sugar);
        megaPkg.addItem(flour);
        megaPkg.addItem(salt);
        megaPkg.addItem(tea);
        megaPkg.addItem(coffee);
        megaPkg.addItem(spices);
        megaPkg.addItem(pasta);
        
        // ==================== CREATE CUSTOM PACKAGES ====================
        
        // Custom Package 1: Mix of individual items
        CustomPackage customPkg = new CustomPackage("Weekly Essentials");
        customPkg.addItem(rice);
        customPkg.addItem(oil);
        customPkg.addItem(sugar);
        customPkg.addItem(tea);
        
        // Custom Package 2: Contains preset package + individual items
        CustomPackage customPkg2 = new CustomPackage("Monthly Supply");
        customPkg2.addPresetPackage(smallPkg);
        customPkg2.addItem(sugar);
        customPkg2.addItem(tea);
        customPkg2.addItem(coffee);
        
        // Custom Package 3: Contains custom package + preset package + items (deep nesting)
        CustomPackage customPkg3 = new CustomPackage("Ultimate Bundle");
        customPkg3.addCustomPackage(customPkg);  // Contains custom package
        customPkg3.addPresetPackage(familyPkg);   // Contains preset package
        customPkg3.addItem(coffee);               // Contains individual item
        customPkg3.addItem(pasta);
        
        // Custom Package 4: Contains another custom package (nested custom packages)
        CustomPackage customPkg4 = new CustomPackage("Super Saver");
        customPkg4.addCustomPackage(customPkg2);  // This contains smallPkg + items
        customPkg4.addItem(pasta);
        customPkg4.addItem(spices);
        
        // ==================== DISPLAY ALL PACKAGES ====================
        
        System.out.println("=== PRESET PACKAGES ===\n");
        
        System.out.println("1. Small Package:");
        smallPkg.display(0);
        System.out.println("   Total: $" + String.format("%.2f", smallPkg.getPrice()) + 
                          " | " + String.format("%.2f", smallPkg.getWeight()) + "kg\n");
        
        System.out.println("2. Family Package:");
        familyPkg.display(0);
        System.out.println("   Total: $" + String.format("%.2f", familyPkg.getPrice()) + 
                          " | " + String.format("%.2f", familyPkg.getWeight()) + "kg\n");
        
        System.out.println("3. Mega Package:");
        megaPkg.display(0);
        System.out.println("   Total: $" + String.format("%.2f", megaPkg.getPrice()) + 
                          " | " + String.format("%.2f", megaPkg.getWeight()) + "kg\n");
        
        System.out.println("\n=== CUSTOM PACKAGES ===\n");
        
        System.out.println("1. Weekly Essentials (Individual items only):");
        customPkg.display(0);
        System.out.println("   Total: $" + String.format("%.2f", customPkg.getPrice()) + 
                          " | " + String.format("%.2f", customPkg.getWeight()) + "kg\n");
        
        System.out.println("2. Monthly Supply (Preset + Items):");
        customPkg2.display(0);
        System.out.println("   Total: $" + String.format("%.2f", customPkg2.getPrice()) + 
                          " | " + String.format("%.2f", customPkg2.getWeight()) + "kg\n");
        
        System.out.println("3. Ultimate Bundle (Custom + Preset + Items - Deep Nesting):");
        customPkg3.display(0);
        System.out.println("   Total: $" + String.format("%.2f", customPkg3.getPrice()) + 
                          " | " + String.format("%.2f", customPkg3.getWeight()) + "kg\n");
        
        System.out.println("4. Super Saver (Nested Custom Packages):");
        customPkg4.display(0);
        System.out.println("   Total: $" + String.format("%.2f", customPkg4.getPrice()) + 
                          " | " + String.format("%.2f", customPkg4.getWeight()) + "kg\n");
        
        // ==================== DEMONSTRATE FLEXIBILITY ====================
        System.out.println("=== DEMONSTRATING COMPOSITE PATTERN FLEXIBILITY ===\n");
        
        // Create a new custom package dynamically
        CustomPackage dynamicPkg = new CustomPackage("Dynamic Package");
        dynamicPkg.addCustomPackage(customPkg3);  // Add complex nested package
        dynamicPkg.addItem(salt);
        
        System.out.println("Dynamic Package (contains Ultimate Bundle + Salt):");
        dynamicPkg.display(0);
        System.out.println("   Total: $" + String.format("%.2f", dynamicPkg.getPrice()) + 
                          " | " + String.format("%.2f", dynamicPkg.getWeight()) + "kg\n");
        
        // Show that we can treat all packages uniformly
        System.out.println("=== UNIFORM TREATMENT OF ALL PACKAGES ===\n");
        List<Package> allPackages = new ArrayList<>();
        allPackages.add(rice);                    // Leaf
        allPackages.add(smallPkg);                // Preset Composite
        allPackages.add(customPkg);              // Custom Composite
        allPackages.add(customPkg4);              // Deep nested Composite
        
        double grandTotal = 0;
        double grandWeight = 0;
        
        for (Package pkg : allPackages) {
            System.out.println(pkg.getName() + ": $" + 
                             String.format("%.2f", pkg.getPrice()) + " | " + 
                             String.format("%.2f", pkg.getWeight()) + "kg");
            grandTotal += pkg.getPrice();
            grandWeight += pkg.getWeight();
        }
        
        System.out.println("\nGrand Total: $" + String.format("%.2f", grandTotal) + 
                          " | " + String.format("%.2f", grandWeight) + "kg");
    }
}