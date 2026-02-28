// ==================== IMPLEMENTOR INTERFACE ====================
// This defines the transportation methods (implementation side)
interface TransportMethod {
    String getTransportName();
    double calculateCost(double distance, double weight);
    int estimateDeliveryTime(double distance);
    void dispatch(String orderId, String address);
    void trackOrder(String orderId);
    boolean performSafetyChecks();
}

// ==================== CONCRETE IMPLEMENTORS ====================
// Bike Courier
class BikeCourier implements TransportMethod {
    @Override
    public String getTransportName() {
        return "Bike Courier";
    }
    
    @Override
    public double calculateCost(double distance, double weight) {
        return 2.0 + (distance * 0.5) + (weight * 0.3);
    }
    
    @Override
    public int estimateDeliveryTime(double distance) {
        return (int)(distance / 15 * 60); // 15 km/h average
    }
    
    @Override
    public void dispatch(String orderId, String address) {
        System.out.println("Dispatching bike courier for order: " + orderId);
    }
    
    @Override
    public void trackOrder(String orderId) {
        System.out.println("Tracking bike courier for order: " + orderId);
    }
    
    @Override
    public boolean performSafetyChecks() {
        System.out.println("Performing bike safety checks (helmet, vehicle condition)");
        return true;
    }
}

// Van Delivery
class VanDelivery implements TransportMethod {
    @Override
    public String getTransportName() {
        return "Van Delivery";
    }
    
    @Override
    public double calculateCost(double distance, double weight) {
        return 5.0 + (distance * 0.8) + (weight * 0.2);
    }
    
    @Override
    public int estimateDeliveryTime(double distance) {
        return (int)(distance / 30 * 60); // 30 km/h average
    }
    
    @Override
    public void dispatch(String orderId, String address) {
        System.out.println("Dispatching van for order: " + orderId);
    }
    
    @Override
    public void trackOrder(String orderId) {
        System.out.println("Tracking van for order: " + orderId);
    }
    
    @Override
    public boolean performSafetyChecks() {
        System.out.println("Performing van safety checks (license, vehicle inspection)");
        return true;
    }
}

// Drone Delivery
class DroneDelivery implements TransportMethod {
    @Override
    public String getTransportName() {
        return "Drone Delivery";
    }
    
    @Override
    public double calculateCost(double distance, double weight) {
        return 3.0 + (distance * 0.4) + (weight * 0.5);
    }
    
    @Override
    public int estimateDeliveryTime(double distance) {
        return (int)(distance / 40 * 60); // 40 km/h average
    }
    
    @Override
    public void dispatch(String orderId, String address) {
        System.out.println("Dispatching drone for order: " + orderId);
    }
    
    @Override
    public void trackOrder(String orderId) {
        System.out.println("Tracking drone for order: " + orderId);
    }
    
    @Override
    public boolean performSafetyChecks() {
        System.out.println("Performing drone safety checks (battery, weather, air traffic)");
        return true;
    }
}

// Robot Delivery
class RobotDelivery implements TransportMethod {
    @Override
    public String getTransportName() {
        return "Robot Delivery";
    }
    
    @Override
    public double calculateCost(double distance, double weight) {
        return 2.5 + (distance * 0.3) + (weight * 0.25);
    }
    
    @Override
    public int estimateDeliveryTime(double distance) {
        return (int)(distance / 10 * 60); // 10 km/h average
    }
    
    @Override
    public void dispatch(String orderId, String address) {
        System.out.println("Dispatching delivery robot for order: " + orderId);
    }
    
    @Override
    public void trackOrder(String orderId) {
        System.out.println("Tracking delivery robot for order: " + orderId);
    }
    
    @Override
    public boolean performSafetyChecks() {
        System.out.println("Performing robot safety checks (sensors, path clearance)");
        return true;
    }
}

// ==================== ABSTRACTION ====================
// This defines the delivery types (abstraction side)
abstract class DeliveryType {
    protected TransportMethod transportMethod;
    
    public DeliveryType(TransportMethod transportMethod) {
        this.transportMethod = transportMethod;
    }
    
    public void setTransportMethod(TransportMethod transportMethod) {
        this.transportMethod = transportMethod;
    }
    
    public abstract String getDeliveryTypeName();
    public abstract int getMaxDeliveryTime();
    
    public double calculatePrice(double distance, double weight) {
        return transportMethod.calculateCost(distance, weight);
    }
    
    public int estimateDeliveryTime(double distance) {
        int baseTime = transportMethod.estimateDeliveryTime(distance);
        return Math.min(baseTime, getMaxDeliveryTime());
    }
    
    public void processOrder(String orderId, String address, double distance, double weight) {
        System.out.println("\n=== Processing " + getDeliveryTypeName() + " ===");
        System.out.println("Using: " + transportMethod.getTransportName());
        
        if (!transportMethod.performSafetyChecks()) {
            System.out.println("Safety checks failed! Order cancelled.");
            return;
        }
        
        double cost = calculatePrice(distance, weight);
        int deliveryTime = estimateDeliveryTime(distance);
        
        System.out.println("Order ID: " + orderId);
        System.out.println("Distance: " + distance + " km");
        System.out.println("Weight: " + weight + " kg");
        System.out.println("Cost: $" + String.format("%.2f", cost));
        System.out.println("Estimated Delivery Time: " + deliveryTime + " minutes");
        System.out.println("Max Delivery Time: " + getMaxDeliveryTime() + " minutes");
        
        transportMethod.dispatch(orderId, address);
        transportMethod.trackOrder(orderId);
    }
}

// ==================== REFINED ABSTRACTIONS ====================
// Standard Delivery (within 24 hours = 1440 minutes)
class StandardDelivery extends DeliveryType {
    public StandardDelivery(TransportMethod transportMethod) {
        super(transportMethod);
    }
    
    @Override
    public String getDeliveryTypeName() {
        return "Standard Delivery";
    }
    
    @Override
    public int getMaxDeliveryTime() {
        return 1440; // 24 hours in minutes
    }
}

// Express Delivery (within 4 hours = 240 minutes)
class ExpressDelivery extends DeliveryType {
    public ExpressDelivery(TransportMethod transportMethod) {
        super(transportMethod);
    }
    
    @Override
    public String getDeliveryTypeName() {
        return "Express Delivery";
    }
    
    @Override
    public int getMaxDeliveryTime() {
        return 240; // 4 hours in minutes
    }
    
    @Override
    public double calculatePrice(double distance, double weight) {
        // Express delivery has 50% premium
        return super.calculatePrice(distance, weight) * 1.5;
    }
}

// Scheduled Delivery (at chosen time slot)
class ScheduledDelivery extends DeliveryType {
    private String timeSlot;
    
    public ScheduledDelivery(TransportMethod transportMethod, String timeSlot) {
        super(transportMethod);
        this.timeSlot = timeSlot;
    }
    
    @Override
    public String getDeliveryTypeName() {
        return "Scheduled Delivery (" + timeSlot + ")";
    }
    
    @Override
    public int getMaxDeliveryTime() {
        return 1440; // 24 hours in minutes
    }
    
    @Override
    public double calculatePrice(double distance, double weight) {
        // Scheduled delivery has 20% premium
        return super.calculatePrice(distance, weight) * 1.2;
    }
}

// ==================== MAIN SYSTEM ====================
public class ZBazarDeliverySystem {
    public static void main(String[] args) {
        System.out.println("=== ZBazar Online Grocery Platform ===\n");
        
        // Create transport methods
        TransportMethod bike = new BikeCourier();
        TransportMethod van = new VanDelivery();
        TransportMethod drone = new DroneDelivery();
        TransportMethod robot = new RobotDelivery();
        
        // Create delivery types with different transport methods
        DeliveryType standardBike = new StandardDelivery(bike);
        DeliveryType expressDrone = new ExpressDelivery(drone);
        DeliveryType scheduledVan = new ScheduledDelivery(van, "2:00 PM - 4:00 PM");
        DeliveryType standardRobot = new StandardDelivery(robot);
        
        // Process orders
        standardBike.processOrder("ORD001", "123 Main St", 5.0, 2.5);
        expressDrone.processOrder("ORD002", "456 Oak Ave", 8.0, 1.0);
        scheduledVan.processOrder("ORD003", "789 Pine Rd", 12.0, 5.0);
        standardRobot.processOrder("ORD004", "Smart Community Gate 1", 2.0, 3.0);
        
        // Demonstrate flexibility: Change transport method dynamically
        System.out.println("\n=== Demonstrating Bridge Pattern Flexibility ===");
        System.out.println("Switching Express Delivery from Drone to Bike...");
        expressDrone.setTransportMethod(bike);
        expressDrone.processOrder("ORD005", "321 Elm St", 3.0, 1.5);
        
        // Adding new transport method is easy - just create a new class
        System.out.println("\n=== Adding New Transport Method (Autonomous Vehicle) ===");
        TransportMethod autoVehicle = new AutonomousVehicle();
        DeliveryType expressAuto = new ExpressDelivery(autoVehicle);
        expressAuto.processOrder("ORD006", "555 Tech Blvd", 10.0, 4.0);
    }
}

// Example of easily adding a new transport method
class AutonomousVehicle implements TransportMethod {
    @Override
    public String getTransportName() {
        return "Autonomous Vehicle";
    }
    
    @Override
    public double calculateCost(double distance, double weight) {
        return 4.0 + (distance * 0.6) + (weight * 0.3);
    }
    
    @Override
    public int estimateDeliveryTime(double distance) {
        return (int)(distance / 35 * 60); // 35 km/h average
    }
    
    @Override
    public void dispatch(String orderId, String address) {
        System.out.println("Dispatching autonomous vehicle for order: " + orderId);
    }
    
    @Override
    public void trackOrder(String orderId) {
        System.out.println("Tracking autonomous vehicle for order: " + orderId);
    }
    
    @Override
    public boolean performSafetyChecks() {
        System.out.println("Performing autonomous vehicle safety checks (AI systems, sensors)");
        return true;
    }
}