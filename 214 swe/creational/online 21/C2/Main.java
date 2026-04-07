import java.util.*;

// abstract products
interface Letter {
    void print();
}

interface Resume {
    void print();
}

// concrete products: formal
class FormalLetter implements Letter {
    public void print() {
        System.out.println("printing a formal letter for professional use.");
    }
}

class FormalResume implements Resume {
    public void print() {
        System.out.println("printing a formal resume for professional use.");
    }
}

// concrete products: informal
class InformalLetter implements Letter {
    public void print() {
        System.out.println("printing a informal letter for professional use.");
    }
}

class InformalResume implements Resume {
    public void print() {
        System.out.println("printing a informal resume for professional use.");
    }
}

// abstract factory: would use abstract class if there's a shared behavior of
// the objects
interface DocumentFactory {
    Letter createLetter();

    Resume createResume();
}

// concrete factories
class FormalDocumentFactory implements DocumentFactory {
    public Letter createLetter() {
        return new FormalLetter();
    }

    public Resume createResume() {
        return new FormalResume();
    }
}

class InormalDocumentFactory implements DocumentFactory {
    public Letter createLetter() {
        return new InformalLetter();
    }

    public Resume createResume() {
        return new InformalResume();
    }
}

// client
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("choose your pref format: formal or informal->");
        String choice = sc.nextLine();
        DocumentFactory ft;
        if (choice.equalsIgnoreCase("formal"))
            ft = new FormalDocumentFactory();
        else
            ft = new InormalDocumentFactory();
        System.out.println("now choose letter or resume: ");
        choice = sc.nextLine();
        if (choice.equalsIgnoreCase("letter")) {
            Letter letter = ft.createLetter();
            letter.print();
        } else if (choice.equalsIgnoreCase("resume")) {
            Resume resume = ft.createResume();
            resume.print();
        }
    }
}