import java.util.ArrayList;
import java.util.List;

interface ComputerComponent {
    double getPrice();
}

class HardwareComponent implements ComputerComponent {

    private String name;
    private double price;

    HardwareComponent(String name, double price) {
        this.name = name;
        this.price = price;
    }

    public double getPrice() {
        return price;
    }

    public String getName() {
        return name;
    }
}

class Bundle implements ComputerComponent {

    private String bundleName;
    private List<ComputerComponent> components = new ArrayList<>();

    Bundle(String bundleName) {
        this.bundleName = bundleName;
    }

    public void add(ComputerComponent component) {
        components.add(component);
    }

    public void remove(ComputerComponent component) {
        components.remove(component);
    }

    public double getPrice() {
        double total = 0;
        for (ComputerComponent c : components) {
            total += c.getPrice();
        }
        return total;
    }

    public String getName() {
        return bundleName;
    }
}

public class online_secA2 {

    public static void main(String[] args) {

        // Individual components
        HardwareComponent cpu = new HardwareComponent("CPU", 300);
        HardwareComponent ram = new HardwareComponent("RAM", 150);
        HardwareComponent gpu = new HardwareComponent("GPU", 500);
        HardwareComponent ssd = new HardwareComponent("SSD", 200);

        // Basic Gaming Bundle
        Bundle basicGaming = new Bundle("Basic Gaming Setup");
        basicGaming.add(cpu);
        basicGaming.add(ram);
        basicGaming.add(gpu);

        // Ultimate Gaming Bundle (bundle inside bundle)
        Bundle ultimateGaming = new Bundle("Ultimate Gaming Setup");
        ultimateGaming.add(basicGaming);
        ultimateGaming.add(ssd);

        // Individual purchase
        System.out.println("CPU Price: $" + cpu.getPrice());

        // Bundle prices
        System.out.println("Basic Gaming Setup Price: $" +
                basicGaming.getPrice());

        System.out.println("Ultimate Gaming Setup Price: $" +
                ultimateGaming.getPrice());

        // Remove component
        basicGaming.remove(ram);

        System.out.println(
                "Basic Gaming Setup after removing RAM: $" +
                basicGaming.getPrice());
    }
}
