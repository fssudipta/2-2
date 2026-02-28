// Component interface representing the basic hardware component
interface Component {
    double getPrice();

    String getDescription();
}

// Concrete Component representing individual hardware components
class HardwareComponent implements Component {
    private String name;
    private double price;

    public HardwareComponent(String name, double price) {
        this.name = name;
        this.price = price;
    }

    @Override
    public double getPrice() {
        return price;
    }

    @Override
    public String getDescription() {
        return name;
    }
}

abstract class ComponentDecorator implements Component {
    protected Component component;

    public ComponentDecorator(Component component) {
        this.component = component;
    }
}

class WarrantyDecorator extends ComponentDecorator {

    public WarrantyDecorator(Component component) {
        super(component);
    }

    public double getPrice() {
        return component.getPrice() + 50;
    }

    public String getDescription() {
        return component.getDescription() + " + Extended Warranty";
    }
}

class InstallationDecorator extends ComponentDecorator {

    public InstallationDecorator(Component component) {
        super(component);
    }

    public double getPrice() {
        return component.getPrice() + 30;
    }

    public String getDescription() {
        return component.getDescription() + " + Installation Service";
    }
}

class PerformanceBoostDecorator extends ComponentDecorator {

    public PerformanceBoostDecorator(Component component) {
        super(component);
    }

    public double getPrice() {
        return component.getPrice() + 100;
    }

    public String getDescription() {
        return component.getDescription() + " + Performance Boost";
    }
}

public class online_secB2 {

    public static void main(String[] args) {

        // Base component
        Component cpu = new HardwareComponent("CPU", 300);

        // Add warranty
        cpu = new WarrantyDecorator(cpu);

        // Add installation
        cpu = new InstallationDecorator(cpu);

        // Add performance boost
        cpu = new PerformanceBoostDecorator(cpu);

        System.out.println("Component: " + cpu.getDescription());
        System.out.println("Total Price: $" + cpu.getPrice());
    }
}
