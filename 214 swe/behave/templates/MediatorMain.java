import java.util.*;

// 1. The Mediator Interface
interface ChatControl {
    void dispatch(String msg, Colleague user);
}

// 2. The Colleague (Abstract Participant)
abstract class Colleague {
    protected ChatControl mediator;
    public String name;

    public Colleague(ChatControl m, String n) {
        this.mediator = m;
        this.name = n;
    }

    public abstract void receive(String msg);
}

// 3. Concrete Mediator
class ChatRoom implements ChatControl {
    private List<Colleague> users = new ArrayList<>();

    public void addUser(Colleague u) {
        users.add(u);
    }

    public void dispatch(String msg, Colleague sender) {
        for (Colleague u : users)
            if (u != sender)
                u.receive(sender.name + ": " + msg);
    }
}

// 4. Concrete Colleague
class User extends Colleague {
    public User(ChatControl m, String n) {
        super(m, n);
    }

    public void send(String msg) {
        mediator.dispatch(msg, this);
    }

    public void receive(String msg) {
        System.out.println("[" + name + " got]: " + msg);
    }
}

// 5. The Client (Main)
public class MediatorMain {
    public static void main(String[] args) {
        ChatRoom room = new ChatRoom();
        User alice = new User(room, "Alice");
        User bob = new User(room, "Bob");

        room.addUser(alice);
        room.addUser(bob);

        alice.send("Hey Bob!"); // Alice doesn't call Bob; she calls the room (Mediator)
    }
}