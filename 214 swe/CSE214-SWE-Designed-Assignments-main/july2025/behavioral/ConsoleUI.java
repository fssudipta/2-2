import java.util.InputMismatchException;
import java.util.Scanner;

public class ConsoleUI {
    private final RegistrarSystem registrar;
    private final Scanner scanner = new Scanner(System.in);

    public ConsoleUI(RegistrarSystem registrar) {
        this.registrar = registrar;
    }

    public void start() {
        while (true) {
            System.out.println("\n=== University Course Registration System ===");
            System.out.println("1. Student mode");
            System.out.println("2. Admin mode");
            System.out.println("0. Exit");
            System.out.print("Choose: ");
            String choice = scanner.nextLine().trim();
            switch (choice) {
                case "1":
                    studentMode();
                    break;
                case "2":
                    adminMode();
                    break;
                case "0":
                    System.out.println("Goodbye!");
                    return;
                default:
                    System.out.println("Invalid option.");
            }
        }
    }

    private void studentMode() {
        System.out.print("Enter Student ID: ");
        String id = scanner.nextLine().trim();
        Student s = registrar.getStudent(id);
        if (s == null) {
            System.out.println("Student not found.");
            return;
        }
        while (true) {
            System.out.println("\n--- Student Mode: " + s.name + " (" + s.id + ") ---");
            System.out.println("1. List available courses");
            System.out.println("2. Add course by code");
            System.out.println("3. Drop course by code");
            System.out.println("4. View my schedule");
            System.out.println("0. Back");
            System.out.print("Choose: ");
            String c = scanner.nextLine().trim();
            switch (c) {
                case "1":
                    listAvailableCourses();
                    break;
                case "2":
                    System.out.print("Course code: ");
                    String addCode = scanner.nextLine().trim();
                    Course courseToAdd = registrar.getCourse(addCode);
                    if (courseToAdd == null) {
                        System.out.println("Course not found.");
                        break;
                    }
                    s.enrollIn(courseToAdd);
                    // if failed due to FULL, suggest waitlist
                    if (courseToAdd.status == CourseStatus.FULL) {
                        System.out.print("Enroll failed. Waitlist instead? (y/n): ");
                        String yn = scanner.nextLine().trim().toLowerCase();
                        if (yn.equals("y")) {
                            s.waitlistFor(courseToAdd);
                        }
                    }
                    break;
                case "3":
                    System.out.print("Course code: ");
                    String dropCode = scanner.nextLine().trim();
                    Course courseToDrop = registrar.getCourse(dropCode);
                    if (courseToDrop == null) {
                        System.out.println("Course not found.");
                        break;
                    }
                    s.dropCourse(courseToDrop);
                    break;
                case "4":
                    s.printSchedule();
                    break;
                case "0":
                    return;
                default:
                    System.out.println("Invalid option.");
            }
        }
    }

    private void adminMode() {
        while (true) {
            System.out.println("\n--- Admin Mode ---");
            System.out.println("1. List ALL courses");
            System.out.println("2. Change course status");
            System.out.println("3. Set course capacity");
            System.out.println("4. Print course roster");
            System.out.println("5. Print course waitlist");
            System.out.println("0. Back");
            System.out.print("Choose: ");
            String c = scanner.nextLine().trim();
            switch (c) {
                case "1":
                    listAllCourses();
                    break;
                case "2":
                    System.out.print("Course code: ");
                    String code = scanner.nextLine().trim();
                    Course course = registrar.getCourse(code);
                    if (course == null) { System.out.println("Course not found."); break; }
                    System.out.println("Available statuses: DRAFT, OPEN, FULL, CLOSED, CANCELLED");
                    System.out.print("New status: ");
                    String statusStr = scanner.nextLine().trim();
                    try {
                        CourseStatus newStatus = CourseStatus.valueOf(statusStr);
                        // Use interactive method that can prompt for capacity when closing FULL courses
                        course.setStatusAdminInteractive(newStatus, scanner);
                    } catch (IllegalArgumentException e) {
                        System.out.println("Invalid status.");
                    }
                    break;
                case "3":
                    System.out.print("Course code: ");
                    String codeCap = scanner.nextLine().trim();
                    Course courseCap = registrar.getCourse(codeCap);
                    if (courseCap == null) { System.out.println("Course not found."); break; }
                    System.out.print("New capacity: ");
                    try {
                        int cap = Integer.parseInt(scanner.nextLine().trim());
                        courseCap.setCapacity(cap);
                    } catch (NumberFormatException e) {
                        System.out.println("Invalid number.");
                    }
                    break;
                case "4":
                    System.out.print("Course code: ");
                    String codeR = scanner.nextLine().trim();
                    Course courseR = registrar.getCourse(codeR);
                    if (courseR == null) { System.out.println("Course not found."); break; }
                    courseR.printRoster();
                    break;
                case "5":
                    System.out.print("Course code: ");
                    String codeW = scanner.nextLine().trim();
                    Course courseW = registrar.getCourse(codeW);
                    if (courseW == null) { System.out.println("Course not found."); break; }
                    courseW.printWaitlist();
                    break;
                case "0":
                    return;
                default:
                    System.out.println("Invalid option.");
            }
        }
    }

    private void listAvailableCourses() {
        System.out.println("Available courses (visible to students):");
        for (Course c : registrar.getAllCourses()) {
            if (c.isVisibleToStudents()) {
                System.out.println("  " + c.code + " - " + c.title + " | status=" + c.status + " | cap=" + c.getCapacity() + " | enrolled=" + c.getEnrolledCount() + " | waitlist=" + c.getWaitlistCount());
            }
        }
    }

    private void listAllCourses() {
        System.out.println("All courses:");
        for (Course c : registrar.getAllCourses()) {
            System.out.println("  " + c.code + " - " + c.title + " | status=" + c.status + " | cap=" + c.getCapacity() + " | enrolled=" + c.getEnrolledCount() + " | waitlist=" + c.getWaitlistCount());
        }
    }
}
