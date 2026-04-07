interface Processor {
    String getSpecs();
}

interface Display {
    String getSpecs();
}

// concrete products: processor
class IntelXeon implements Processor {
    public String getSpecs() {
        return "Intel Xeon (professional Grade)";
    }
}

class ARMProcessor implements Processor {
    public String getSpecs() {
        return "ARM Processor (Power Efficient)";
    }
}

// concrete products: display
class IPSDisplay implements Display {
    public String getSpecs() {
        return "IPS Display (High Color Accuracy)";
    }
}

class OLEDDisplay implements Display {
    public String getSpecs() {
        return "OLED Display (Deep Blacks & Lightweight)";
    }
}

// final computer class
class Computer {
    private String modelName;
    private Processor processor;
    private Display display;

    public Computer(String modelName, Processor processor, Display display) {
        this.modelName = modelName;
        this.processor = processor;
        this.display = display;
    }

    public void showConfiguration() {
        System.out.println("Model: " + modelName);
        System.out.println("Processor: " + processor.getSpecs());
        System.out.println("Display: " + display.getSpecs());
        System.out.println("damn, it works");
    }
}

// abstract factory
interface ComputerFactory {
    Processor createProcessor();

    Display createDisplay();

    String getModelName();
}

// concrete factories
class WorkProFactory implements ComputerFactory {
    public Processor createProcessor() {
        return new IntelXeon();
    }

    public Display createDisplay() {
        return new IPSDisplay();
    }

    public String getModelName() {
        return "WorkPro";
    }
}

class LiteMaxFactory implements ComputerFactory {
    public Processor createProcessor() {
        return new ARMProcessor();
    }

    public Display createDisplay() {
        return new OLEDDisplay();
    }

    public String getModelName() {
        return "LiteMax";
    }
}

// client code
public class Main {
    public static void main(String[] args) {
        ComputerFactory factory;
        factory = new WorkProFactory();
        Computer workPro = new Computer(factory.getModelName(), factory.createProcessor(), factory.createDisplay());
        workPro.showConfiguration();
    }
}