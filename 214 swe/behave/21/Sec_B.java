interface LightState {
    String color();

    int seconds();

    LightState next();
}

class Red implements LightState {
    public String color() {
        return "RED   - Stop!";
    }

    public int seconds() {
        return 5;
    }

    public LightState next() {
        return new Yellow();
    }
}

class Yellow implements LightState {
    public String color() {
        return "YELLOW - Caution!";
    }

    public int seconds() {
        return 2;
    }

    public LightState next() {
        return new Green();
    }
}

class Green implements LightState {
    public String color() {
        return "GREEN  - Go!";
    }

    public int seconds() {
        return 10;
    }

    public LightState next() {
        return new Red();
    }
}

class TrafficLight {
    LightState state = new Red();

    void run(int steps) throws InterruptedException {
        for (int i = 0; i < steps; i++) {
            System.out.println("[Light] " + state.color() + " (" + state.seconds() + "s)");
            Thread.sleep(state.seconds() * 1000L);
            state = state.next();
        }
    }
}

public class Sec_B {
    public static void main(String[] args) throws InterruptedException {
        new TrafficLight().run(6); // 2 full cycles
    }
}