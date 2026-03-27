abstract class HospitalVisit {
    final void visit(String name) {
        System.out.println("[Check-In] Patient: " + name + " | ID: V" + (int) (Math.random() * 1000));
        System.out.println("[Vitals] Temp: 98.6F | BP: 120/80");
        assess();
        treat();
        System.out.println("[Discharge] Patient discharged. Notes: " + notes());
        System.out.println();
    }

    abstract void assess();

    abstract void treat();

    abstract String notes();
}

class General extends HospitalVisit {
    void assess() {
        System.out.println("[Assessment] Doctor performs normal diagnosis.");
    }

    void treat() {
        System.out.println("[Treatment] Prescribe standard medicine.");
    }

    String notes() {
        return "Follow up in 1 week.";
    }
}

class Pediatrics extends HospitalVisit {
    void assess() {
        System.out.println("[Assessment] Check symptoms ensuring child comfort.");
    }

    void treat() {
        System.out.println("[Treatment] Child-safe medicine + reassurance.");
    }

    String notes() {
        return "Stay cheerful! Return if fever persists.";
    }
}

class Emergency extends HospitalVisit {
    void assess() {
        System.out.println("[Assessment] Quick triage (urgent/non-urgent).");
    }

    void treat() {
        System.out.println("[Treatment] Immediate emergency procedure.");
    }

    String notes() {
        return "Monitor vitals every hour.";
    }
}

public class C1_hospital {
    public static void main(String[] args) {
        new General().visit("Alice");
        new Pediatrics().visit("Tommy");
        new Emergency().visit("Bob");
    }
}