import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Collection;

public class RegistrarSystem {
    private final Map<String, Student> students = new HashMap<>();
    private final Map<String, Course> courses = new HashMap<>();

    // public void addStudent(Student s) {
    // if (s != null) students.put(s.id, s);
    // }

    // public void addCourse(Course c) {
    // if (c != null) courses.put(c.code, c);
    // }

    public Student getStudent(String id) {
        return students.get(id);
    }

    public Course getCourse(String code) {
        return courses.get(code);
    }

    public Collection<Student> getAllStudents() {
        return students.values();
    }

    public Collection<Course> getAllCourses() {
        return courses.values();
    }

    public void addStudent(Student s) {
        s.setMediator(this);
        students.put(s.id, s);
    }

    public void addCourse(Course c) {
        c.setMediator(this);
        courses.put(c.code, c);
    }

    // Coordinating Enrollment
    public void enrollStudent(String studentId, String courseCode) {
        Student s = students.get(studentId);
        Course c = courses.get(courseCode);
        if (s != null && c != null) {
            if (c.tryEnroll(s)) {
                s.addEnrolledCourseDirect(c);
            }
        }
    }

    public void waitlistStudent(String studentId, String courseCode) {
        Student s = students.get(studentId);
        Course c = courses.get(courseCode);
        if (s != null && c != null) {
            if (c.addToWaitlist(s)) {
                s.addWaitlistCourseDirect(c);
            }
        }
    }

    public void dropStudent(String studentId, String courseCode) {
        Student s = students.get(studentId);
        Course c = courses.get(courseCode);
        if (s != null && c != null) {
            if (c.dropStudent(s)) {
                s.removeCourseDirect(c);
            }
        }
    }

    // Sync helpers for Course to call
    public void syncPromotion(Student s, Course c) {
        s.addEnrolledCourseDirect(c);
    }

    public void notifyCancellation(Course c, List<Student> affected) {
        for (Student s : affected)
            s.removeCourseDirect(c);
    }
}
