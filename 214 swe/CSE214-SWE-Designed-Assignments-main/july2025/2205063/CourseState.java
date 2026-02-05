import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public interface CourseState {
    boolean tryEnroll(Course course, Student s);

    boolean addToWaitlist(Course course, Student s);

    void setStatus(Course course, CourseStatus newStatus);

    void setCapacity(Course course, int newCapacity);

    boolean isVisible();

    CourseStatus getStatus();
}

abstract class AbstractCourseState implements CourseState {
    @Override
    public void setCapacity(Course course, int newCapacity) {
        course.applyCapacityChange(newCapacity);
    }

    protected void handlePromotion(Course course) {
        if (course.getEnrolledCount() < course.getCapacity() && !course.getWaitlist().isEmpty()) {
            Student promoted = course.getWaitlist().poll();
            if (promoted != null) {
                course.getEnrolled().add(promoted);
                // Coordination handled by Mediator in actual flow, but internal state must
                // update
                System.out.println("Promoted from waitlist: " + promoted.name + " into " + course.code);
                course.getMediator().syncPromotion(promoted, course);
            }
        }
    }
}

class DraftState extends AbstractCourseState {
    public CourseStatus getStatus() {
        return CourseStatus.DRAFT;
    }

    public boolean isVisible() {
        return false;
    }

    public boolean tryEnroll(Course course, Student s) {
        System.out.println("Cannot enroll; course is DRAFT: " + course.code);
        return false;
    }

    public boolean addToWaitlist(Course course, Student s) {
        System.out.println("Cannot waitlist; course is DRAFT: " + course.code);
        return false;
    }

    public void setStatus(Course course, CourseStatus newStatus) {
        if (newStatus == CourseStatus.OPEN) {
            course.setState(new OpenState());
            System.out.println(course.code + " transitioned DRAFT -> OPEN");
        } else if (newStatus == CourseStatus.CLOSED) {
            course.setState(new ClosedState());
            System.out.println(course.code + " transitioned DRAFT -> CLOSED");
        } else if (newStatus == CourseStatus.CANCELLED) {
            course.performCancellation();
        } else {
            System.out.println("Invalid transition from DRAFT to " + newStatus);
        }
    }
}

class OpenState extends AbstractCourseState {
    public CourseStatus getStatus() {
        return CourseStatus.OPEN;
    }

    public boolean isVisible() {
        return true;
    }

    public boolean tryEnroll(Course course, Student s) {
        if (course.getEnrolledCount() < course.getCapacity()) {
            course.getEnrolled().add(s);
            System.out.println("Enrolled: " + s.name + " in " + course.code);
            if (course.getEnrolledCount() >= course.getCapacity()) {
                course.setState(new FullState());
                System.out.println(course.code + " is now FULL.");
            }
            return true;
        }
        course.setState(new FullState());
        return false;
    }

    public boolean addToWaitlist(Course course, Student s) {
        System.out.println("Course is OPEN; try enrolling instead: " + course.code);
        return false;
    }

    public void setStatus(Course course, CourseStatus newStatus) {
        if (newStatus == CourseStatus.CLOSED) {
            course.setState(new ClosedState());
            System.out.println(course.code + " transitioned OPEN -> CLOSED");
        } else if (newStatus == CourseStatus.DRAFT) {
            course.setState(new DraftState());
            System.out.println(course.code + " transitioned OPEN -> DRAFT");
        } else if (newStatus == CourseStatus.CANCELLED) {
            course.performCancellation();
        } else {
            System.out.println("Invalid transition from OPEN to " + newStatus);
        }
    }
}

class FullState extends AbstractCourseState {
    public CourseStatus getStatus() {
        return CourseStatus.FULL;
    }

    public boolean isVisible() {
        return true;
    }

    public boolean tryEnroll(Course course, Student s) {
        System.out.println("Cannot enroll; course is FULL. You may waitlist: " + course.code);
        return false;
    }

    public boolean addToWaitlist(Course course, Student s) {
        course.getWaitlist().add(s);
        System.out.println("Waitlisted: " + s.name + " for " + course.code);
        return true;
    }

    public void setStatus(Course course, CourseStatus newStatus) {
        if (newStatus == CourseStatus.CLOSED) {
            course.performCloseWithWaitlist(course.getCapacity());
        } else if (newStatus == CourseStatus.CANCELLED) {
            course.performCancellation();
        } else {
            System.out.println("Invalid transition from FULL to " + newStatus + " (FULL->OPEN is automatic on drop)");
        }
    }
}

class ClosedState extends AbstractCourseState {
    public CourseStatus getStatus() {
        return CourseStatus.CLOSED;
    }

    public boolean isVisible() {
        return true;
    }

    public boolean tryEnroll(Course course, Student s) {
        System.out.println("Cannot enroll; course is CLOSED: " + course.code);
        return false;
    }

    public boolean addToWaitlist(Course course, Student s) {
        System.out.println("Cannot waitlist; course is CLOSED: " + course.code);
        return false;
    }

    public void setStatus(Course course, CourseStatus newStatus) {
        if (newStatus == CourseStatus.OPEN) {
            course.setState(new OpenState());
            System.out.println(course.code + " transitioned CLOSED -> OPEN");
        } else if (newStatus == CourseStatus.DRAFT) {
            course.setState(new DraftState());
            System.out.println(course.code + " transitioned CLOSED -> DRAFT");
        } else if (newStatus == CourseStatus.CANCELLED) {
            course.performCancellation();
        } else {
            System.out.println("Invalid transition from CLOSED to " + newStatus);
        }
    }
}

class CancelledState extends AbstractCourseState {
    public CourseStatus getStatus() {
        return CourseStatus.CANCELLED;
    }

    public boolean isVisible() {
        return false;
    }

    public boolean tryEnroll(Course course, Student s) {
        System.out.println("Cannot enroll; course is CANCELLED: " + course.code);
        return false;
    }

    public boolean addToWaitlist(Course course, Student s) {
        System.out.println("Cannot waitlist; course is CANCELLED: " + course.code);
        return false;
    }

    public void setStatus(Course course, CourseStatus newStatus) {
        if (newStatus == CourseStatus.DRAFT) {
            course.setState(new DraftState());
            System.out.println(course.code + " transitioned CANCELLED -> DRAFT (reinstating course)");
        } else {
            System.out.println("Invalid: CANCELLED can only transition to DRAFT for " + course.code);
        }
    }
}