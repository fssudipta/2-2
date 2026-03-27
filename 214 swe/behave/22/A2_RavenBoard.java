import java.util.*;

interface Observer {
    void update(String msg);
}

class Commander implements Observer {
    public void update(String msg) {
        System.out.println("[Commander] '" + msg + "' -> Assess threat!");
    }
}

class Scouts implements Observer {
    public void update(String msg) {
        System.out.println("[Scouts] '" + msg + "' -> Dispatch riders!");
    }
}

class SupplyTeam implements Observer {
    public void update(String msg) {
        System.out.println("[SupplyTeam] '" + msg + "' -> Update inventory!");
    }
}

class RavenBoard {
    List<Observer> subs = new ArrayList<>();

    void subscribe(Observer o) {
        subs.add(o);
        System.out.println(o.getClass().getSimpleName() + " subscribed.");
    }

    void unsubscribe(Observer o) {
        subs.remove(o);
        System.out.println(o.getClass().getSimpleName() + " left.");
    }

    void post(String msg) {
        System.out.println("\n[Board] New message: '" + msg + "'");
        for (Observer o : subs)
            o.update(msg);
    }
}

public class A2_RavenBoard {
    public static void main(String[] args) {
        RavenBoard board = new RavenBoard();
        Observer cmd = new Commander(), sc = new Scouts(), sup = new SupplyTeam();

        board.subscribe(cmd);
        board.subscribe(sc);
        board.subscribe(sup);
        board.post("Enemy spotted near the river");

        board.unsubscribe(sc);
        board.post("Winter supplies running low");

        board.subscribe(sc);
        board.post("Ships seen in the east");
    }
}