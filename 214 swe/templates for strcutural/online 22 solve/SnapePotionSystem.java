import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

// Component Interface
interface Potion {
    String getName();
    double getCost();
    int getWeight();
    List<String> getIngredients();
}

// Concrete Component - Base Potion with Maker's Solution
class BasePotion implements Potion {
    private String name;
    
    public BasePotion(String name) {
        this.name = name;
    }
    
    @Override
    public String getName() {
        return name;
    }
    
    @Override
    public double getCost() {
        // Maker's Solution: white spirit ($1.23/10g) + castor oil ($2.47/10g)
        // 25g of each = 2.5 * (1.23 + 2.47) = $9.25
        return 2.5 * (1.23 + 2.47);
    }
    
    @Override
    public int getWeight() {
        // 25g white spirit + 25g castor oil = 50g
        return 50;
    }
    
    @Override
    public List<String> getIngredients() {
        List<String> ingredients = new ArrayList<>();
        ingredients.add("white spirit (25g) - $1.23/10g");
        ingredients.add("castor oil (25g) - $2.47/10g");
        return ingredients;
    }
}

// Decorator Abstract Class
abstract class PotionDecorator implements Potion {
    protected Potion potion;
    
    public PotionDecorator(Potion potion) {
        this.potion = potion;
    }
    
    @Override
    public String getName() {
        return potion.getName();
    }
    
    @Override
    public double getCost() {
        return potion.getCost();
    }
    
    @Override
    public int getWeight() {
        return potion.getWeight();
    }
    
    @Override
    public List<String> getIngredients() {
        return potion.getIngredients();
    }
}

// Concrete Decorators for each special ingredient

class PoisonIvyDecorator extends PotionDecorator {
    public PoisonIvyDecorator(Potion potion) {
        super(potion);
    }
    
    @Override
    public double getCost() {
        // 25g of poison ivy at $3.38/10g = 2.5 * 3.38 = $8.45
        return super.getCost() + (2.5 * 3.38);
    }
    
    @Override
    public int getWeight() {
        return super.getWeight() + 25;
    }
    
    @Override
    public List<String> getIngredients() {
        List<String> ingredients = super.getIngredients();
        ingredients.add("poison ivy (25g) - $3.38/10g");
        return ingredients;
    }
}

class UnicornHornDecorator extends PotionDecorator {
    public UnicornHornDecorator(Potion potion) {
        super(potion);
    }
    
    @Override
    public double getCost() {
        // 25g of unicorn horn at $6.31/10g = 2.5 * 6.31 = $15.775
        return super.getCost() + (2.5 * 6.31);
    }
    
    @Override
    public int getWeight() {
        return super.getWeight() + 25;
    }
    
    @Override
    public List<String> getIngredients() {
        List<String> ingredients = super.getIngredients();
        ingredients.add("unicorn horn (25g) - $6.31/10g");
        return ingredients;
    }
}

class DragonKidneyDecorator extends PotionDecorator {
    public DragonKidneyDecorator(Potion potion) {
        super(potion);
    }
    
    @Override
    public double getCost() {
        // 25g of dragon kidney at $5.86/10g = 2.5 * 5.86 = $14.65
        return super.getCost() + (2.5 * 5.86);
    }
    
    @Override
    public int getWeight() {
        return super.getWeight() + 25;
    }
    
    @Override
    public List<String> getIngredients() {
        List<String> ingredients = super.getIngredients();
        ingredients.add("dragon kidney (25g) - $5.86/10g");
        return ingredients;
    }
}

class ChineseChompingCabbageDecorator extends PotionDecorator {
    public ChineseChompingCabbageDecorator(Potion potion) {
        super(potion);
    }
    
    @Override
    public double getCost() {
        // 25g of Chinese chomping cabbage at $4.13/10g = 2.5 * 4.13 = $10.325
        return super.getCost() + (2.5 * 4.13);
    }
    
    @Override
    public int getWeight() {
        return super.getWeight() + 25;
    }
    
    @Override
    public List<String> getIngredients() {
        List<String> ingredients = super.getIngredients();
        ingredients.add("Chinese chomping cabbage (25g) - $4.13/10g");
        return ingredients;
    }
}

// Main System Class
public class SnapePotionSystem {
    
    public static Potion createPotion(String potionName) {
        BasePotion basePotion = new BasePotion(potionName);
        
        switch (potionName.toLowerCase()) {
            case "polyjuice potion":
                return new PoisonIvyDecorator(basePotion);
            case "felix felicis":
                return new UnicornHornDecorator(basePotion);
            case "veritaserum":
                return new DragonKidneyDecorator(basePotion);
            case "skele-gro":
                return new ChineseChompingCabbageDecorator(basePotion);
            default:
                return basePotion;
        }
    }
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("=== Professor Snape's Potion Brewing System ===\n");
        System.out.println("Available Potions:");
        System.out.println("1. Polyjuice Potion");
        System.out.println("2. Felix Felicis");
        System.out.println("3. Veritaserum");
        System.out.println("4. Skele-Gro\n");
        
        System.out.print("Enter number of different potions to brew: ");
        int numPotions = scanner.nextInt();
        scanner.nextLine(); // consume newline
        
        double totalCost = 0;
        int totalWastedWeight = 0;
        
        for (int i = 0; i < numPotions; i++) {
            System.out.print("\nEnter potion name: ");
            String potionName = scanner.nextLine();
            
            System.out.print("Enter number of jars: ");
            int numJars = scanner.nextInt();
            scanner.nextLine(); // consume newline
            
            System.out.print("Enter wasted ingredients (in grams): ");
            int wastedGrams = scanner.nextInt();
            scanner.nextLine(); // consume newline
            
            // Create the potion using Decorator Pattern
            Potion potion = createPotion(potionName);
            
            // Calculate costs and penalties
            double costPerJar = potion.getCost();
            double totalPotionCost = costPerJar * numJars;
            int penaltyPoints = wastedGrams * 2; // 2 points per gram wasted
            
            totalCost += totalPotionCost;
            totalWastedWeight += wastedGrams;
            
            // Display results
            System.out.println("\n--- Potion Details ---");
            System.out.println("Potion Name: " + potion.getName());
            System.out.println("Number of Jars: " + numJars);
            System.out.println("Ingredients:");
            for (String ingredient : potion.getIngredients()) {
                System.out.println("  - " + ingredient);
            }
            System.out.println("Cost per Jar: $" + String.format("%.2f", costPerJar));
            System.out.println("Total Cost: $" + String.format("%.2f", totalPotionCost));
            System.out.println("Wasted Ingredients: " + wastedGrams + "g");
            System.out.println("Penalty Points: " + penaltyPoints);
        }
        
        System.out.println("\n=== Summary ===");
        System.out.println("Total Cost for All Potions: $" + String.format("%.2f", totalCost));
        System.out.println("Total Wasted Ingredients: " + totalWastedWeight + "g");
        System.out.println("Total Penalty Points: " + (totalWastedWeight * 2));
        
        scanner.close();
    }
}