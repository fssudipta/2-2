interface Channel {
    void send(String customer, String msg);
}

class Email implements Channel {
    public void send(String c, String m) {
        System.out.println("[Email]  -> " + c + ": " + m);
    }
}

class SMS implements Channel {
    public void send(String c, String m) {
        System.out.println("[SMS]    -> " + c + ": " + m);
    }
}

class AppPush implements Channel {
    public void send(String c, String m) {
        System.out.println("[App]    -> " + c + ": " + m);
    }
}
// Extensible: add WhatsApp here without changing anything else

class NotifyService {
    Channel channel;

    NotifyService(Channel c) {
        channel = c;
    }

    void setChannel(Channel c) {
        channel = c;
    }

    void notify(String customer, String msg) {
        channel.send(customer, msg);
    }
}

public class Online_3_A2 {
    public static void main(String[] args) {
        NotifyService svc = new NotifyService(new Email());
        svc.notify("Alice", "Transaction of $500 done.");

        svc.setChannel(new SMS());
        svc.notify("Alice", "Low balance warning!");

        svc.setChannel(new AppPush());
        svc.notify("Alice", "Promo: 10% cashback!");
    }
}