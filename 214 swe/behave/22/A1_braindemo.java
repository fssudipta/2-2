interface Tier {
    String getTiername();

    int getCoverage();

    Tier promote();

    Tier demote();
}

// concrete states
class Common implements Tier {
    public String getTiername() {
        return "common";
    }

    public int getCoverage() {
        return 10;
    }

    public Tier promote() {
        return new Plus();
    }

    public Tier demote() {
        return this;
    }
}

class Plus implements Tier {
    public String getTiername() {
        return "Plus";
    }

    public int getCoverage() {
        return 50;
    }

    public Tier promote() {
        return new Lux();
    }

    public Tier demote() {
        return new Common();
    }
}

class Lux implements Tier {
    public String getTiername() {
        return "Luxxx";
    }

    public int getCoverage() {
        return 50;
    }

    public Tier promote() {
        return this;
    }

    public Tier demote() {
        return new Plus();
    }
}

class BrainSub {
    private Tier tier;
    private Tier preLux;
    private String mood = null;

    public BrainSub() {
        this.tier = new Common();
    }

    public void travelCheck(int km) {
        if (km <= tier.getCoverage()) {
            System.out.println(tier.getTiername() + ": patient is stable");
        } else
            System.out.println(tier.getTiername() + ": patient is unstable. bring back into coverage.");
    }

    public void activateLux(int hours) {
        if (tier instanceof Lux) {
            System.out.println("already in lux");
            return;
        }
        preLux = tier;
        tier = new Lux();
        System.out.println("lux activated for hrs(): " + hours);
        try {
            Thread.sleep(hours * 1000L);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        tier = preLux;
        System.out.println("back to frens");
    }

    public void setMood(String mood) {
        if (tier instanceof Lux) {
            this.mood = mood;
            System.out.println("Mood set to: " + mood);
        } else
            System.out.println("Mood control unavailable.");
    }

    public void promote() {
        tier = tier.promote();
        System.out.println("promoted tier: " + tier.getTiername());
    }

    public void demote() {
        tier = tier.demote();
        System.out.println("demoted tier: " + tier.getTiername());
    }

    public String getTier() {
        return tier.getTiername();
    }
}

public class A1_braindemo {
    public static void main(String[] args) {
        BrainSub sub = new BrainSub();
        System.out.println("Starting tier: " + sub.getTier());
        // gemini marsi etay
        sub.travelCheck(5); // STABLE (Common: 0-10km)
        sub.travelCheck(15); // UNSTABLE

        sub.promote(); // Common -> Plus
        sub.travelCheck(30); // STABLE (Plus: 0-50km)
        sub.travelCheck(60); // UNSTABLE

        sub.promote(); // Plus -> Lux
        sub.promote(); // Lux -> Lux (no change)

        sub.setMood("calm"); // Works in Lux
        sub.travelCheck(40); // STABLE

        sub.demote(); // Lux -> Plus
        sub.setMood("happy"); // Mood control unavailable

        System.out.println("\n--- Activating Lux for 2 seconds (simulating 2 hours) ---");
        sub.activateLux(2); // temporarily Lux, then back to Plus

        sub.demote(); // Plus -> Common
        sub.demote();
    }
}