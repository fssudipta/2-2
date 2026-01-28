public class Main {
    public static void main(String[] args) {
        RegistrarSystem reg = new RegistrarSystem();

        // Create 20 students
        Student s1 = new Student("S001", "Alice");
        Student s2 = new Student("S002", "Bob");
        Student s3 = new Student("S003", "Charlie");
        Student s4 = new Student("S004", "Diana");
        Student s5 = new Student("S005", "Evan");
        Student s6 = new Student("S006", "Fiona");
        Student s7 = new Student("S007", "George");
        Student s8 = new Student("S008", "Hannah");
        Student s9 = new Student("S009", "Ian");
        Student s10 = new Student("S010", "Julia");
        Student s11 = new Student("S011", "Kevin");
        Student s12 = new Student("S012", "Laura");
        Student s13 = new Student("S013", "Mike");
        Student s14 = new Student("S014", "Nina");
        Student s15 = new Student("S015", "Oscar");
        Student s16 = new Student("S016", "Paula");
        Student s17 = new Student("S017", "Quinn");
        Student s18 = new Student("S018", "Rachel");
        Student s19 = new Student("S019", "Steve");
        Student s20 = new Student("S020", "Tina");
        
        reg.addStudent(s1); reg.addStudent(s2); reg.addStudent(s3); reg.addStudent(s4);
        reg.addStudent(s5); reg.addStudent(s6); reg.addStudent(s7); reg.addStudent(s8);
        reg.addStudent(s9); reg.addStudent(s10); reg.addStudent(s11); reg.addStudent(s12);
        reg.addStudent(s13); reg.addStudent(s14); reg.addStudent(s15); reg.addStudent(s16);
        reg.addStudent(s17); reg.addStudent(s18); reg.addStudent(s19); reg.addStudent(s20);

        // Create 7 courses
        Course cse101 = new Course("CSE101", "Intro to Programming", 2, CourseStatus.OPEN);
        Course cse201 = new Course("CSE201", "Data Structures", 3, CourseStatus.OPEN);
        Course cse220 = new Course("CSE220", "Algorithms", 2, CourseStatus.CLOSED);
        Course cse310 = new Course("CSE310", "Operating Systems", 3, CourseStatus.OPEN);
        Course cse330 = new Course("CSE330", "Computer Networks", 2, CourseStatus.OPEN);
        Course cse499 = new Course("CSE499", "Senior Project", 1, CourseStatus.DRAFT);
        Course math101 = new Course("MATH101", "Calculus I", 5, CourseStatus.OPEN);
        
        reg.addCourse(cse101); reg.addCourse(cse201); reg.addCourse(cse220);
        reg.addCourse(cse310); reg.addCourse(cse330); reg.addCourse(cse499);
        reg.addCourse(math101);

        // Sample enrollments
        s1.enrollIn(cse101);
        s2.enrollIn(cse101);
        s3.enrollIn(cse101); // will fail; course full, suggest waitlist
        s3.waitlistFor(cse101);

        s1.enrollIn(cse201);

        System.out.println();

        ConsoleUI ui = new ConsoleUI(reg);
        ui.start();
    }
}
