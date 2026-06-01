import java.util.ArrayList;
import java.util.List;

// The Component
interface Employee {
    void showDetails(String prefix);
}
class IndividualContributor implements Employee {
    private String name;
    private String position;

    public IndividualContributor(String name, String position) {
        this.name = name;
        this.position = position;
    }

    @Override
    public void showDetails(String prefix) {
        System.out.println(prefix + "|-- " + name + " (" + position + ")");
    }
}
class Manager implements Employee {
    private String name;
    private String position;
    private List<Employee> subordinates = new ArrayList<>();

    public Manager(String name, String position) {
        this.name = name;
        this.position = position;
    }

    public void addSubordinate(Employee e) {
        subordinates.add(e);
    }

    @Override
    public void showDetails(String prefix) {
        System.out.println(prefix + "+ " + name + " [" + position + "]");
        for (Employee e : subordinates) {
            e.showDetails(prefix + "   ");
        }
    }
}
public class CompanyHierarchy {
    public static void main(String[] args) {
        // 1. Create Top Level
        Manager md = new Manager("Alice", "Managing Director");

        // 2. Technical Division
        Manager techManager = new Manager("Bob", "Technical Manager");
        for (int i = 1; i <= 5; i++) {
            techManager.addSubordinate(new IndividualContributor("Dev " + i, "Developer"));
        }

        // 3. Administration Division
        Manager adminManager = new Manager("Charlie", "Admin Manager");
        for (int i = 1; i <= 3; i++) {
            adminManager.addSubordinate(new IndividualContributor("Exec " + i, "Executive"));
        }

        // 4. Finance Division
        Manager financeManager = new Manager("Diana", "Finance Manager");
        financeManager.addSubordinate(new IndividualContributor("Officer 1", "Officer"));
        financeManager.addSubordinate(new IndividualContributor("Officer 2", "Officer"));

        // 5. Build Final Tree
        md.addSubordinate(techManager);
        md.addSubordinate(adminManager);
        md.addSubordinate(financeManager);

        // Show Full Hierarchy
        md.showDetails("");
    }
}