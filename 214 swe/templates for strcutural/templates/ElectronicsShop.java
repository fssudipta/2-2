// the implementation interface
interface Device{
    void enable();
    void disable();
    void setVolume(int percent);
    void getChannel();
}
//concrete implementation first
class TV implements Device{
    @Override
    public void enable(){
        System.out.println("TV: power on");
    }
    @Override
    public void disable(){
        System.out.println("TV: power off");
    }
    @Override
    public void setVolume(int percent){
        System.out.println("TV: volume is set to "+percent);
    }
    @Override
    public void getChannel(){
        System.out.println("TV: channel is 6");
    }
}
//concrete implementation second
class Radio implements Device{
    @Override
    public void enable(){
        System.out.println("radio: power on");
    }
    @Override
    public void disable(){
        System.out.println("radio: power off");
    }
    @Override
    public void setVolume(int percent){
        System.out.println("radio: volume is set to "+percent);
    }
    @Override
    public void getChannel(){
        System.out.println("radio: channel is 98.4");
    }
}

// the abstraction: defines what user can do
abstract class RemoteControl{
    protected Device device; //bridge connection
    public RemoteControl(Device device){
        this.device=device;
    }
    public void togglePower(){
        device.enable();
    }
    public void volumeDown(){
        device.setVolume(10);
    }
    public void volumeUp(){
        device.setVolume(90);
    }
}
//fancy remote adding new features
class AdvancedRemote extends RemoteControl{
    public AdvancedRemote(Device device){
        super(device);
    }
}

//gpt marsi
public class ElectronicsShop {
    public static void main(String[] args) {
        // 1. Create a Device (Implementation)
        Device tv = new TV();
        Device radio = new Radio();

        // 2. Create a Remote (Abstraction) and bridge them
        RemoteControl basicRemote = new RemoteControl(tv);
        AdvancedRemote advancedRemote = new AdvancedRemote(radio);

        // 3. Use the Basic Remote on the TV
        System.out.println("--- Using Basic Remote on TV ---");
        basicRemote.togglePower();
        basicRemote.volumeUp();

        // 4. Use the Advanced Remote on the Radio
        System.out.println("\n--- Using Advanced Remote on Radio ---");
        advancedRemote.togglePower();
        advancedRemote.mute();

        // 5. Switch the Device dynamically!
        System.out.println("\n--- Switching TV to Advanced Remote ---");
        advancedRemote = new AdvancedRemote(tv); // Same remote, new device
        advancedRemote.togglePower();
    }
}