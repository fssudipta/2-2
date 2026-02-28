interface Device {
    void turnOn();
    void turnOff();
    void setVolume(int volume);
}

class TV implements Device {

    @Override
    public void turnOn() {
        System.out.println("TV is ON");
    }

    @Override
    public void turnOff() {
        System.out.println("TV is OFF");
    }

    @Override
    public void setVolume(int volume) {
        System.out.println("TV volume set to " + volume);
    }
}

class Radio implements Device {

    @Override
    public void turnOn() {
        System.out.println("Radio is ON");
    }

    @Override
    public void turnOff() {
        System.out.println("Radio is OFF");
    }

    @Override
    public void setVolume(int volume) {
        System.out.println("Radio volume set to " + volume);
    }
}

abstract class RemoteControl {
    protected Device device;

    public RemoteControl(Device device) {
        this.device = device;
    }

    abstract void power();
}

class BasicRemote extends RemoteControl {

    public BasicRemote(Device device) {
        super(device);
    }

    @Override
    public void power() {
        device.turnOn();
    }
}

class AdvancedRemote extends RemoteControl {

    public AdvancedRemote(Device device) {
        super(device);
    }

    @Override
    public void power() {
        device.turnOn();
    }

    public void mute() {
        device.setVolume(0);
        System.out.println("Device muted");
    }
}

public class BridgeDP {
    public static void main(String[] args) {

        Device tv = new TV();
        RemoteControl basicRemote = new BasicRemote(tv);
        basicRemote.power();

        Device radio = new Radio();
        AdvancedRemote advancedRemote = new AdvancedRemote(radio);
        advancedRemote.power();
        advancedRemote.mute();
    }
}

