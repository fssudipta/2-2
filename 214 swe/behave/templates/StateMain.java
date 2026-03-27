// 1. The State Interface
interface State { void pressButton(VendingMachine machine); }

// 2. Concrete States
class ReadyState implements State {
    public void pressButton(VendingMachine m) {
        System.out.println("Dispensing product...");
        m.setState(new OutOfOrderState()); // State change logic
    }
}

class OutOfOrderState implements State {
    public void pressButton(VendingMachine m) { System.out.println("Machine broken. Call tech support."); }
}

// 3. The Context
class VendingMachine {
    private State current;
    public VendingMachine() { current = new ReadyState(); }
    public void setState(State s) { this.current = s; }
    public void press() { current.pressButton(this); }
}

// 4. The Client (Main)
public class StateMain {
    public static void main(String[] args) {
        VendingMachine vm = new VendingMachine();
        vm.press(); // First press: Dispensing
        vm.press(); // Second press: Out of Order
    }
}