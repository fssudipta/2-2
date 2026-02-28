// the common interface for all objects
interface Coffee{
    String getDescription();
    double getCost();
}

//the base object
class DarkRoast implements Coffee{
    @Override
    public String getDescription(){
        return "Dark Roast Coffee";
    }
    @Override
    public double getCost(){
        return 3.00;
    }
}

//the base decorator that holds a reference to a coffee object
abstract class CoffeeDecorator implements Coffee{
    protected Coffee decoratedCoffee;
    public CoffeeDecorator(Coffee kaffee){
        this.decoratedCoffee=kaffee;
    }
    @Override
    public double getCost(){
        return decoratedCoffee.getCost();
    }
    @Override
    public String getDescription(){
        return decoratedCoffee.getDescription();
    }
}

// concrete decorators
// decorator 1: milk
class Milk extends CoffeeDecorator{
    public Milk(Coffee coffee){
        super(coffee);
    }
    @Override
    public String getDescription(){
        return super.getDescription()+", Milk";
    }
    @Override
    public double getCost(){
        return super.getCost()+0.50;
    }
}

// Decorator 2: Sugar
class Sugar extends CoffeeDecorator {
    public Sugar(Coffee coffee) {
        super(coffee);
    }

    @Override
    public String getDescription() {
        return super.getDescription() + ", Sugar";
    }

    @Override
    public double getCost() {
        return super.getCost() + 0.20;
    }
}

// Decorator 3: Whip
class Whip extends CoffeeDecorator {
    public Whip(Coffee coffee) {
        super(coffee);
    }

    @Override
    public String getDescription() {
        return super.getDescription() + ", Whip";
    }

    @Override
    public double getCost() {
        return super.getCost() + 0.30;
    }
}

public class CoffeeShop {
    public static void main(String[] args) {
        // 1. Order a simple Dark Roast
        Coffee myCoffee = new DarkRoast();
        System.out.println(myCoffee.getDescription() + " $" + myCoffee.getCost());
        // Output: Dark Roast Coffee $3.0

        // 2. Add Milk (Wrap the coffee)
        myCoffee = new Milk(myCoffee);
        System.out.println(myCoffee.getDescription() + " $" + myCoffee.getCost());
        // Output: Dark Roast Coffee, Milk $3.5

        // 3. Add Sugar (Wrap the milk-wrapped coffee)
        myCoffee = new Sugar(myCoffee);
        System.out.println(myCoffee.getDescription() + " $" + myCoffee.getCost());
        // Output: Dark Roast Coffee, Milk, Sugar $3.7

        // 4. Add Whip (Wrap the previous stack)
        myCoffee = new Whip(myCoffee);
        System.out.println(myCoffee.getDescription() + " $" + myCoffee.getCost());
        // Output: Dark Roast Coffee, Milk, Sugar, Whip $4.0
    }
}