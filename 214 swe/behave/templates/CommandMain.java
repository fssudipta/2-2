// --- THE COMMAND INTERFACE ---
// This is the "Slip". It just has one job: Execute.
interface Command {
    void execute();

    void undo(); // Commands are great for undoing!
}

// --- THE RECEIVER ---
// This is the "Chef". This class has the actual logic.
// Notice it doesn't know anything about the "Command" pattern.
class SmartLight {
    public void turnOn() {
        System.out.println("[Receiver] Chef is cooking... I mean, Light is ON.");
    }

    public void turnOff() {
        System.out.println("[Receiver] Light is OFF.");
    }
}

// --- CONCRETE COMMANDS ---
// These wrap the Receiver and tell it what to do.
class LightOnCommand implements Command {
    private SmartLight light; // The Chef

    public LightOnCommand(SmartLight light) {
        this.light = light;
    }

    @Override
    public void execute() {
        System.out.println("[Command] Executing: Telling the light to turn on...");
        light.turnOn();
    }

    @Override
    public void undo() {
        System.out.println("[Command] Undoing: Telling the light to turn off...");
        light.turnOff();
    }
}

// --- THE INVOKER ---
// This is the "Waiter". It holds the command and triggers it.
// It doesn't know WHAT the command does, only how to call execute().
class RemoteControl {
    private Command lastCommand;

    public void submit(Command command) {
        System.out.println("[Invoker] Waiter received the order. Pressing button...");
        this.lastCommand = command;
        command.execute();
    }

    public void pressUndo() {
        if (lastCommand != null) {
            System.out.println("[Invoker] Waiter is undoing the last action...");
            lastCommand.undo();
        }
    }
}

// --- THE CLIENT (MAIN) ---
// You are the Customer. You link the Chef to the Order.
public class CommandMain {
    public static void main(String[] args) {
        // 1. Create the Receiver (The guy who actually does the work)
        SmartLight livingRoomLight = new SmartLight();

        // 2. Create the Command and tell it who its Receiver is
        // "Here is a slip that says 'Turn On' for the 'Living Room Light'"
        LightOnCommand switchOn = new LightOnCommand(livingRoomLight);

        // 3. Create the Invoker (The UI or Remote)
        RemoteControl remote = new RemoteControl();

        // 4. The Action
        System.out.println("--- CLIENT: I want the light on! ---");
        remote.submit(switchOn);

        System.out.println("\n--- CLIENT: Wait, I changed my mind! ---");
        remote.pressUndo();
    }
}