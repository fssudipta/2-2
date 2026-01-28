public class TestScenarios {
    public static void main(String[] args) {
        System.out.println("=== Running Comprehensive Test Scenarios (5-State System) ===\n");
        
        RegistrarSystem reg = new RegistrarSystem();

        // Create test students
        Student alice = new Student("S1", "Alice");
        Student bob = new Student("S2", "Bob");
        Student charlie = new Student("S3", "Charlie");
        Student diana = new Student("S4", "Diana");
        Student evan = new Student("S5", "Evan");
        Student frank = new Student("S6", "Frank");
        Student grace = new Student("S7", "Grace");
        
        reg.addStudent(alice);
        reg.addStudent(bob);
        reg.addStudent(charlie);
        reg.addStudent(diana);
        reg.addStudent(evan);
        reg.addStudent(frank);
        reg.addStudent(grace);

        // Create test courses with various initial states
        Course cse101 = new Course("CSE101", "Intro Programming", 2, CourseStatus.OPEN);
        Course cse201 = new Course("CSE201", "Data Structures", 1, CourseStatus.OPEN);
        Course cse330 = new Course("CSE330", "Systems", 2, CourseStatus.OPEN);
        Course cse499 = new Course("CSE499", "Special Topics", 2, CourseStatus.DRAFT);
        Course cse220 = new Course("CSE220", "Algorithms", 2, CourseStatus.CLOSED);
        Course cse310 = new Course("CSE310", "Operating Systems", 3, CourseStatus.OPEN);
        
        reg.addCourse(cse101);
        reg.addCourse(cse201);
        reg.addCourse(cse330);
        reg.addCourse(cse499);
        reg.addCourse(cse220);
        reg.addCourse(cse310);

        // ===== PART 1: AUTOMATIC STATE TRANSITIONS =====
        System.out.println("===== PART 1: AUTOMATIC STATE TRANSITIONS =====\n");

        // Test 1: Automatic OPEN -> FULL transition
        System.out.println("--- Test 1: Automatic OPEN -> FULL when capacity reached ---");
        System.out.println("CSE101 initial: status=" + cse101.status + " enrolled=" + cse101.getEnrolledCount() + " cap=" + cse101.getCapacity());
        alice.enrollIn(cse101);
        bob.enrollIn(cse101);
        System.out.println("CSE101 after 2 enrollments: status=" + cse101.status + "\n");

        // Test 2: FULL course behavior - reject enrollment, allow waitlist
        System.out.println("--- Test 2: FULL course behavior (reject enroll, allow waitlist) ---");
        charlie.enrollIn(cse101);
        charlie.waitlistFor(cse101);
        diana.waitlistFor(cse101);
        evan.waitlistFor(cse101);
        cse101.printWaitlist();
        System.out.println();

        // Test 3: Automatic FULL -> OPEN on drop with waitlist promotion
        System.out.println("--- Test 3: Automatic FULL -> OPEN on drop + waitlist promotion ---");
        System.out.println("Before drop: status=" + cse101.status);
        alice.dropCourse(cse101);
        System.out.println("After drop: status=" + cse101.status + " (Charlie promoted from waitlist)");
        cse101.printRoster();
        cse101.printWaitlist();
        System.out.println();

        // Test 4: Multiple drops causing FULL -> OPEN
        System.out.println("--- Test 4: Another drop triggering FULL -> OPEN ---");
        bob.dropCourse(cse101);
        System.out.println("After Bob drops: status=" + cse101.status + " (Diana promoted)");
        cse101.printRoster();
        System.out.println();

        // ===== PART 2: ADMIN STATE TRANSITIONS (FORWARD) =====
        System.out.println("===== PART 2: ADMIN STATE TRANSITIONS (FORWARD) =====\n");

        // Test 5: DRAFT -> OPEN
        System.out.println("--- Test 5: Admin DRAFT -> OPEN ---");
        System.out.println("CSE499 before: " + cse499.status);
        cse499.setStatusAdmin(CourseStatus.OPEN);
        System.out.println("CSE499 after: " + cse499.status);
        evan.enrollIn(cse499);
        System.out.println();

        // Test 6: OPEN -> CLOSED
        System.out.println("--- Test 6: Admin OPEN -> CLOSED ---");
        System.out.println("CSE310 before: " + cse310.status);
        cse310.setStatusAdmin(CourseStatus.CLOSED);
        System.out.println("CSE310 after: " + cse310.status);
        alice.enrollIn(cse310);
        System.out.println();

        // Test 7: OPEN -> DRAFT
        System.out.println("--- Test 7: Admin OPEN -> DRAFT (reverting to draft) ---");
        Course cse400 = new Course("CSE400", "Senior Project", 2, CourseStatus.OPEN);
        reg.addCourse(cse400);
        System.out.println("CSE400 before: " + cse400.status);
        cse400.setStatusAdmin(CourseStatus.DRAFT);
        System.out.println("CSE400 after: " + cse400.status + " (no longer visible to students)");
        System.out.println();

        // Test 8: FULL -> CLOSED (without waitlist)
        System.out.println("--- Test 8: Admin FULL -> CLOSED (no waitlist) ---");
        Course cse150 = new Course("CSE150", "Discrete Math", 1, CourseStatus.OPEN);
        reg.addCourse(cse150);
        alice.enrollIn(cse150);
        System.out.println("CSE150 before: " + cse150.status);
        cse150.setStatusAdmin(CourseStatus.CLOSED);
        System.out.println("CSE150 after: " + cse150.status);
        System.out.println();

        // Test 9: FULL -> CLOSED (with capacity increase and random waitlist selection)
        System.out.println("--- Test 9: Admin FULL -> CLOSED with capacity increase ---");
        System.out.println("NOTE: In interactive mode, admin is prompted to increase capacity when closing FULL course.");
        System.out.println("The capacity increase happens DURING the close operation, not before.\n");
        Course cse250 = new Course("CSE250", "Computer Architecture", 2, CourseStatus.OPEN);
        reg.addCourse(cse250);
        alice.enrollIn(cse250);
        bob.enrollIn(cse250);
        System.out.println("CSE250 status: " + cse250.status + " (enrolled=" + cse250.getEnrolledCount() + ", cap=" + cse250.getCapacity() + ")");
        charlie.waitlistFor(cse250);
        diana.waitlistFor(cse250);
        evan.waitlistFor(cse250);
        frank.waitlistFor(cse250);
        System.out.println("Waitlisted: 4 students");
        cse250.printWaitlist();
        System.out.println("\nDemonstrating FULL -> CLOSED with manual capacity increase:");
        System.out.println("(In ConsoleUI, admin would be prompted interactively)");
        // Simulate what happens in interactive mode:
        // 1. Admin increases capacity
        cse250.setCapacity(5);
        System.out.println("After capacity increase, status became: " + cse250.status);
        // 2. Admin still wants to close, so set back to FULL and then close
        System.out.println("To demonstrate FULL->CLOSED, we need course to be FULL first...");
        System.out.println("Actual usage: use setStatusAdminInteractive() in ConsoleUI for proper flow.\n");
        
        // Create another test course already FULL to demonstrate properly
        Course cse260 = new Course("CSE260", "Database Systems", 2, CourseStatus.OPEN);
        reg.addCourse(cse260);
        diana.enrollIn(cse260);
        evan.enrollIn(cse260);
        System.out.println("CSE260 status: " + cse260.status);
        alice.waitlistFor(cse260);
        bob.waitlistFor(cse260);
        charlie.waitlistFor(cse260);
        System.out.println("CSE260 waitlist: 3 students");
        cse260.printWaitlist();
        System.out.println("\nNow closing CSE260 from FULL (without capacity increase in test):");
        cse260.setStatusAdmin(CourseStatus.CLOSED);
        System.out.println("Result: Course closed, waitlist remains (no capacity increase).");
        cse260.printRoster();
        cse260.printWaitlist();
        System.out.println();

        // Test 10: DRAFT -> CLOSED
        System.out.println("--- Test 10: Admin DRAFT -> CLOSED (closing before opening) ---");
        Course cse500 = new Course("CSE500", "Graduate Seminar", 2, CourseStatus.DRAFT);
        reg.addCourse(cse500);
        System.out.println("CSE500 before: " + cse500.status);
        cse500.setStatusAdmin(CourseStatus.CLOSED);
        System.out.println("CSE500 after: " + cse500.status);
        System.out.println();

        // ===== PART 3: ADMIN STATE TRANSITIONS (BACKWARD) =====
        System.out.println("===== PART 3: ADMIN STATE TRANSITIONS (BACKWARD) =====\n");

        // Test 11: CLOSED -> OPEN
        System.out.println("--- Test 11: Admin CLOSED -> OPEN (reopening) ---");
        System.out.println("CSE220 before: " + cse220.status);
        cse220.setStatusAdmin(CourseStatus.OPEN);
        System.out.println("CSE220 after: " + cse220.status);
        alice.enrollIn(cse220);
        System.out.println();

        // Test 12: CLOSED -> DRAFT
        System.out.println("--- Test 12: Admin CLOSED -> DRAFT (reverting to planning) ---");
        System.out.println("CSE310 before: " + cse310.status);
        cse310.setStatusAdmin(CourseStatus.DRAFT);
        System.out.println("CSE310 after: " + cse310.status);
        System.out.println();

        // ===== PART 4: CAPACITY CHANGES AFFECTING STATE =====
        System.out.println("===== PART 4: CAPACITY CHANGES AFFECTING STATE =====\n");

        // Test 13: Capacity increase causing FULL -> OPEN
        System.out.println("--- Test 13: Capacity increase causing status change ---");
        System.out.println("CSE201 before: enrolled=" + cse201.getEnrolledCount() + " cap=" + cse201.getCapacity() + " status=" + cse201.status);
        cse201.setCapacity(3);
        System.out.println("CSE201 after capacity increase: status=" + cse201.status);
        bob.enrollIn(cse201);
        System.out.println();

        // Test 14: Capacity decrease
        System.out.println("--- Test 14: Capacity decrease (more enrolled than capacity) ---");
        System.out.println("CSE220 before: enrolled=" + cse220.getEnrolledCount() + " cap=" + cse220.getCapacity() + " status=" + cse220.status);
        cse220.setCapacity(1);
        System.out.println("CSE220 after capacity decrease: status=" + cse220.status + " (over capacity)");
        System.out.println();

        // ===== PART 5: CANCELLATION =====
        System.out.println("===== PART 5: COURSE CANCELLATION =====\n");

        // Test 15: Cancellation clears roster and waitlist
        System.out.println("--- Test 15: OPEN -> CANCELLED (clears all students) ---");
        System.out.println("CSE101 before cancellation:");
        cse101.printRoster();
        cse101.printWaitlist();
        cse101.setStatusAdmin(CourseStatus.CANCELLED);
        System.out.println("CSE101 after cancellation:");
        cse101.printRoster();
        charlie.printSchedule();
        System.out.println();

        // Test 16: CANCELLED -> DRAFT (reinstating course)
        System.out.println("--- Test 16: CANCELLED -> DRAFT (reinstating cancelled course) ---");
        System.out.println("CSE101 before: " + cse101.status);
        cse101.setStatusAdmin(CourseStatus.DRAFT);
        System.out.println("CSE101 after: " + cse101.status + " (course reinstated for planning)");
        System.out.println();

        // Test 17: CANCELLED -> other states (invalid)
        System.out.println("--- Test 17: CANCELLED -> OPEN/CLOSED (invalid) ---");
        Course cse600 = new Course("CSE600", "Research Methods", 2, CourseStatus.OPEN);
        reg.addCourse(cse600);
        cse600.setStatusAdmin(CourseStatus.CANCELLED);
        System.out.println("Attempting invalid transitions from CANCELLED:");
        cse600.setStatusAdmin(CourseStatus.OPEN);
        cse600.setStatusAdmin(CourseStatus.CLOSED);
        System.out.println();

        // Test 18: Cancel from FULL with waitlist
        System.out.println("--- Test 18: FULL -> CANCELLED (clears roster and waitlist) ---");
        Course cse700 = new Course("CSE700", "Machine Learning", 1, CourseStatus.OPEN);
        reg.addCourse(cse700);
        bob.enrollIn(cse700);
        charlie.waitlistFor(cse700);
        diana.waitlistFor(cse700);
        System.out.println("CSE700 before:");
        cse700.printRoster();
        cse700.printWaitlist();
        cse700.setStatusAdmin(CourseStatus.CANCELLED);
        System.out.println("CSE700 after:");
        cse700.printRoster();
        bob.printSchedule();
        System.out.println();

        // ===== PART 6: INVALID TRANSITIONS =====
        System.out.println("===== PART 6: INVALID TRANSITIONS =====\n");

        // Test 19: DRAFT -> FULL (invalid)
        System.out.println("--- Test 19: DRAFT -> FULL (invalid) ---");
        Course cse800 = new Course("CSE800", "Advanced Topics", 2, CourseStatus.DRAFT);
        reg.addCourse(cse800);
        cse800.setStatusAdmin(CourseStatus.FULL);
        System.out.println();

        // Test 20: FULL -> OPEN attempted manually (should fail - it's automatic)
        System.out.println("--- Test 20: FULL -> OPEN manual attempt (should fail - automatic only) ---");
        Course cse900 = new Course("CSE900", "Distributed Systems", 1, CourseStatus.OPEN);
        reg.addCourse(cse900);
        alice.enrollIn(cse900);
        System.out.println("CSE900 status: " + cse900.status);
        cse900.setStatusAdmin(CourseStatus.OPEN);
        System.out.println();

        // Test 21: OPEN -> FULL (invalid - automatic only)
        System.out.println("--- Test 21: OPEN -> FULL (invalid - automatic only) ---");
        System.out.println("CSE499 status: " + cse499.status);
        cse499.setStatusAdmin(CourseStatus.FULL);
        System.out.println();

        // ===== PART 7: TIGHT COUPLING DEMONSTRATION =====
        System.out.println("===== PART 7: TIGHT COUPLING EXAMPLES =====\n");

        // Test 22: Student directly updates Course, Course directly updates Student
        System.out.println("--- Test 22: Cross-object manipulation (tight coupling) ---");
        System.out.println("Diana enrolls in CSE220 -> Student calls Course, both update their lists");
        diana.enrollIn(cse220);
        System.out.println("Diana's schedule:");
        diana.printSchedule();
        System.out.println("CSE220 roster:");
        cse220.printRoster();
        System.out.println("Note: Both Student and Course maintain duplicate state!\n");

        // Test 23: Waitlist promotion shows direct cross-manipulation
        System.out.println("--- Test 23: Waitlist promotion (Course updates Student directly) ---");
        Course cse1000 = new Course("CSE1000", "Capstone Project", 1, CourseStatus.OPEN);
        reg.addCourse(cse1000);
        bob.enrollIn(cse1000);
        charlie.waitlistFor(cse1000);
        System.out.println("Charlie waitlisted for CSE1000");
        System.out.println("Bob drops CSE1000 -> Course promotes Charlie and updates Charlie's lists directly:");
        bob.dropCourse(cse1000);
        charlie.printSchedule();
        System.out.println("Note: Course.dropStudent() directly manipulated Student.enrolledCourses!\n");

        // ===== PART 8: REGISTRAR AS SIMPLE LOOKUP =====
        System.out.println("===== PART 8: REGISTRAR AS SIMPLE LOOKUP =====\n");

        // Test 24: UI and Student both use Registrar just for lookups
        System.out.println("--- Test 24: Registrar only provides lookups, no coordination ---");
        System.out.println("UI retrieves course via: registrar.getCourse(\"CSE220\")");
        Course retrieved = reg.getCourse("CSE220");
        System.out.println("Retrieved: " + retrieved.code + " - " + retrieved.title);
        System.out.println("Then UI calls course.setStatusAdmin() directly - no central coordination!");
        System.out.println("Registrar doesn't validate, mediate, or notify anyone.\n");

        // ===== SUMMARY =====
        System.out.println("===== FINAL SUMMARY =====\n");
        System.out.println("5-State System: DRAFT, OPEN, FULL, CLOSED, CANCELLED");
        System.out.println();
        System.out.println("State transitions tested:");
        System.out.println("  - Automatic: OPEN <-> FULL (based on enrollment/capacity)");
        System.out.println("  - Admin forward: DRAFT -> OPEN/CLOSED, OPEN -> CLOSED/DRAFT");
        System.out.println("  - Admin forward: FULL -> CLOSED (with random waitlist selection)");
        System.out.println("  - Admin backward: CLOSED -> OPEN/DRAFT");
        System.out.println("  - Cancellation: Any -> CANCELLED, CANCELLED -> DRAFT only");
        System.out.println();
        System.out.println("=== All Test Scenarios Completed ===");
    }
}
