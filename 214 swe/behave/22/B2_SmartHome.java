interface Mediator {
    void notify(String sender, String event);
}

class Hub implements Mediator {
    Blinds blinds;
    AC ac;

    public void notify(String sender, String event) {
        System.out.println("  [Hub] from " + sender + ": " + event);
        if (event.equals("HighBrightness"))
            blinds.close();
        else if (event.equals("BlindsClosed"))
            ac.turnOn();
    }
}

class LightSensor {
    Mediator hub;

    LightSensor(Mediator h) {
        hub = h;
    }

    void detect(String level) {
        System.out.println("[LightSensor] " + level);
        hub.notify("LightSensor", level);
    }
}

class Blinds {
    Mediator hub;

    Blinds(Mediator h) {
        hub = h;
    }

    void close() {
        System.out.println("[Blinds] Closing...");
        hub.notify("Blinds", "BlindsClosed");
    }
}

class AC {
    void turnOn() {
        System.out.println("[AC] Turned ON.");
    }
}

public class B2_SmartHome {
    public static void main(String[] args) {
        Hub hub = new Hub();
        hub.blinds = new Blinds(hub);
        hub.ac = new AC();
        LightSensor sensor = new LightSensor(hub);

        sensor.detect("HighBrightness");
    }
}