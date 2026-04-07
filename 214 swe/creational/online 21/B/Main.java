// prduct class
class Meal {
    private String starter;
    private String mainDish;
    private String dessert;

    public void setStarter(String starter)
    {
        this.starter=starter;
    }
    public void setMainDish(String mainDish)
    {
        this.mainDish=mainDish;
    }
    public void setDessert(String dessert)
    {
        this.dessert=dessert;
    }

    public void showMeal(){
        System.out.println("Meal deets: ");
        System.out.println("Starter: "+starter);
        System.out.println("Main dish: "+mainDish);
        System.out.println("Dessert: "+ dessert);
        System.out.println("that's all");
    }
}

//abstract builder

interface MealBuilder {
    void buildStarter();
    void buildMainDish();
    void buildDessert();
    Meal getMeal();
}

//concrete builder for first product
class BengaliMealBuilder implements MealBuilder{
    private Meal meal = new Meal();
    public void buildStarter()
    {
        meal.setStarter("Vegetable");
    }
    public void buildMainDish()
    {
        meal.setMainDish("Chimken curry");
    }
    public void buildDessert()
    {
        meal.setDessert("Sweet curd");
    }
    public Meal getMeal()
    {
        return meal;
    }
}

class ChineseMealBuilder implements MealBuilder{
    private Meal meal = new Meal();
    public void buildStarter()
    {
        meal.setStarter("Soup");
    }
    public void buildMainDish()
    {
        meal.setMainDish("Pecking duck");
    }
    public void buildDessert()
    {
        meal.setDessert("Pudding");
    }
    public Meal getMeal()
    {
        return meal;
    }
}

class Director{
    private MealBuilder builder;
    public void setMealBuilder(MealBuilder builder)
    {
        this.builder=builder;
    }
    public Meal constructMeal(){
        builder.buildStarter();
        builder.buildMainDish();
        builder.buildDessert();
        return builder.getMeal();
    }
}

public class Main{
    public static void main(String[] args) {
        Director waiter=new Director();

        System.out.println("customer orders a bengali meal: ");
        MealBuilder bengali = new BengaliMealBuilder();
        waiter.setMealBuilder(bengali);
        Meal bengaliMeal = waiter.constructMeal();
        bengaliMeal.showMeal();
    }
}