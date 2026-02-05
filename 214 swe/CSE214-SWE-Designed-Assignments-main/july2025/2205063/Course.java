import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

public class Course {
    public final String code;
    public final String title;
    private int capacity;
    public CourseStatus status;
    private CourseState state;
    private final List<Student> enrolled = new ArrayList<>();
    private final LinkedList<Student> waitlist = new LinkedList<>();
    private RegistrarSystem mediator;

    public Course(String code, String title, int capacity, CourseStatus InitStatus) {
        this.code = code;
        this.title = title;
        this.capacity = Math.max(0, capacity);
        setInitialState(InitStatus);
    }

    // initialstate set
    private void setInitialState(CourseStatus status) {
        switch (status) {
            case OPEN:
                this.state = new OpenState();
                break;
            case FULL:
                this.state = new FullState();
                break;
            case CLOSED:
                this.state = new ClosedState();
                break;
            case CANCELLED:
                this.state = new CancelledState();
                break;
            default:
                this.state = new DraftState();
                break;
        }
        this.status = this.state.getStatus();
    }

    public void setMediator(RegistrarSystem mediator) {
        this.mediator = mediator;
    }

    public RegistrarSystem getMediator() {
        return mediator;
    }

    public void setState(CourseState state) {
        this.state = state;
        this.status = state.getStatus();
    }

    public CourseStatus getStatus() {
        return state.getStatus();
    }

    public boolean isVisibleToStudents() {
        return state.isVisible();
        // return status != CourseStatus.DRAFT && status != CourseStatus.CANCELLED;
    }

    // public boolean tryEnroll(Student s) {
    // if (s == null)
    // return false;
    // switch (status) {
    // case OPEN:
    // if (enrolled.contains(s)) {
    // System.out.println("Already enrolled: " + s.name + " in " + code);
    // return true; // no-op
    // }
    // if (enrolled.size() < capacity) {
    // enrolled.add(s);
    // s.addEnrolledCourseDirect(this);
    // System.out.println("Enrolled: " + s.name + " in " + code);
    // if (enrolled.size() >= capacity) {
    // status = CourseStatus.FULL;
    // System.out.println(code + " is now FULL.");
    // }
    // return true;
    // } else {
    // // capacity reached while OPEN -> FULL and suggest waitlist
    // status = CourseStatus.FULL;
    // System.out.println(code + " reached capacity; status set to FULL. Try
    // waitlisting.");
    // return false;
    // }
    // case FULL:
    // System.out.println("Cannot enroll; course is FULL. You may waitlist: " +
    // code);
    // return false;
    // case CLOSED:
    // System.out.println("Cannot enroll; course is CLOSED: " + code);
    // return false;
    // case DRAFT:
    // System.out.println("Cannot enroll; course is DRAFT (not visible): " + code);
    // return false;
    // case CANCELLED:
    // System.out.println("Cannot enroll; course is CANCELLED: " + code);
    // return false;
    // default:
    // return false;
    // }
    // }

    public boolean tryEnroll(Student s) {
        return state.tryEnroll(this, s);
    }

    // public boolean addToWaitlist(Student s) {
    // if (s == null)
    // return false;
    // switch (status) {
    // case FULL:
    // if (enrolled.contains(s)) {
    // System.out.println("Already enrolled; no need to waitlist: " + s.name + " for
    // " + code);
    // return false;
    // }
    // if (waitlist.contains(s)) {
    // System.out.println("Already waitlisted: " + s.name + " for " + code);
    // return false;
    // }
    // waitlist.add(s);
    // s.addWaitlistCourseDirect(this);
    // System.out.println("Waitlisted: " + s.name + " for " + code);
    // return true;
    // case OPEN:
    // System.out.println("Course is OPEN; try enrolling instead: " + code);
    // return false;
    // case CLOSED:
    // case DRAFT:
    // case CANCELLED:
    // System.out.println("Cannot waitlist; course not accepting waitlist: " +
    // code);
    // return false;
    // default:
    // return false;
    // }
    // }

    public boolean addToWaitlist(Student s) {
        return state.addToWaitlist(this, s);
    }

    // public boolean dropStudent(Student s) {
    // if (s == null)
    // return false;
    // boolean changed = false;
    // if (enrolled.contains(s)) {
    // enrolled.remove(s);
    // s.removeCourseDirect(this);
    // System.out.println("Dropped from enrolled: " + s.name + " from " + code);
    // changed = true;

    // // After drop: maybe promote one from waitlist if space
    // if (status != CourseStatus.CANCELLED && status != CourseStatus.DRAFT) {
    // if (enrolled.size() < capacity) {
    // if (!waitlist.isEmpty()) {
    // Student promoted = waitlist.poll();
    // if (promoted != null) {
    // enrolled.add(promoted);
    // promoted.addEnrolledCourseDirect(this);
    // promoted.removeCourseDirect(this); // ensure waitlist removed too
    // System.out.println("Promoted from waitlist: " + promoted.name + " into " +
    // code);
    // }
    // }
    // // Recalculate status: FULL -> OPEN if space
    // if (status == CourseStatus.FULL && enrolled.size() < capacity) {
    // status = CourseStatus.OPEN;
    // System.out.println(code + " status changed to OPEN due to available
    // capacity.");
    // }
    // if (enrolled.size() >= capacity) {
    // status = CourseStatus.FULL;
    // }
    // }
    // }
    // } else if (waitlist.contains(s)) {
    // waitlist.remove(s);
    // s.removeCourseDirect(this);
    // System.out.println("Removed from waitlist: " + s.name + " for " + code);
    // changed = true;
    // } else {
    // System.out.println(s.name + " is neither enrolled nor waitlisted for " +
    // code);
    // }
    // return changed;
    // }

    public boolean dropStudent(Student s) {
        boolean removed = false;
        if (enrolled.contains(s)) {
            enrolled.remove(s);
            System.out.println("Dropped from enrolled: " + s.name + " from " + code);
            removed = true;
            if (getStatus() != CourseStatus.CANCELLED && getStatus() != CourseStatus.DRAFT) {
                if (enrolled.size() < capacity) {
                    // Logic to promote or change state
                    if (!waitlist.isEmpty()) {
                        Student promoted = waitlist.poll();
                        enrolled.add(promoted);
                        mediator.syncPromotion(promoted, this);
                        System.out.println("Promoted from waitlist: " + promoted.name + " into " + code);
                    }
                    if (getStatus() == CourseStatus.FULL && enrolled.size() < capacity) {
                        setState(new OpenState());
                        System.out.println(code + " status changed to OPEN due to available capacity.");
                    }
                }
            }
        } else if (waitlist.contains(s)) {
            waitlist.remove(s);
            System.out.println("Removed from waitlist: " + s.name + " for " + code);
            removed = true;
        }
        return removed;
    }

    // public void setCapacity(int newCapacity) {
    // if (newCapacity < 0)
    // newCapacity = 0;
    // System.out.println("Setting capacity of " + code + " to " + newCapacity);
    // this.capacity = newCapacity;
    // if (status == CourseStatus.CANCELLED) {
    // System.out.println("Course is CANCELLED; capacity change has no effect.");
    // return;
    // }
    // // Adjust status based on capacity and current enrolled
    // if (enrolled.size() < capacity) {
    // if (status != CourseStatus.DRAFT) {
    // status = CourseStatus.OPEN;
    // System.out.println(code + " status changed to OPEN (capacity allows
    // enrollment).");
    // }
    // } else if (enrolled.size() == capacity) {
    // status = CourseStatus.FULL;
    // System.out.println(code + " status changed to FULL (at capacity).");
    // } else {
    // // more enrolled than capacity: keep FULL, admin must resolve
    // status = CourseStatus.FULL;
    // System.out.println(code + " over capacity; remains FULL.");
    // }
    // }

    public void setCapacity(int newCap) {
        state.setCapacity(this, newCap);
    }

    protected void applyCapacityChange(int newCap) {
        this.capacity = Math.max(0, newCap);
        System.out.println("Setting capacity of " + code + " to " + capacity);

        if (getStatus() == CourseStatus.CANCELLED)
            return;

        if (enrolled.size() < capacity) {
            if (getStatus() != CourseStatus.DRAFT) {
                setState(new OpenState());
                System.out.println(code + " status changed to OPEN (capacity allows enrollment).");
            }
        } else if (enrolled.size() == capacity) {
            setState(new FullState());
            System.out.println(code + " status changed to FULL (at capacity).");
        } else {
            setState(new FullState());
            System.out.println(code + " over capacity; remains FULL.");
        }
    }

    // public void setStatusAdmin(CourseStatus newStatus) {
    // if (newStatus == null)
    // return;
    // if (newStatus == status) {
    // System.out.println("No change: " + code + " already " + status);
    // return;
    // }

    // // Enforce transition rules with enhanced flexibility
    // switch (status) {
    // case DRAFT:
    // if (newStatus == CourseStatus.OPEN) {
    // status = CourseStatus.OPEN;
    // System.out.println(code + " transitioned DRAFT -> OPEN");
    // } else if (newStatus == CourseStatus.CLOSED) {
    // status = CourseStatus.CLOSED;
    // System.out.println(code + " transitioned DRAFT -> CLOSED");
    // } else if (newStatus == CourseStatus.CANCELLED) {
    // cancelCourse();
    // } else {
    // System.out.println("Invalid transition from DRAFT to " + newStatus);
    // }
    // break;
    // case OPEN:
    // if (newStatus == CourseStatus.CLOSED) {
    // status = CourseStatus.CLOSED;
    // System.out.println(code + " transitioned OPEN -> CLOSED");
    // } else if (newStatus == CourseStatus.DRAFT) {
    // status = CourseStatus.DRAFT;
    // System.out.println(code + " transitioned OPEN -> DRAFT");
    // } else if (newStatus == CourseStatus.CANCELLED) {
    // cancelCourse();
    // } else {
    // System.out.println("Invalid transition from OPEN to " + newStatus);
    // }
    // break;
    // case FULL:
    // if (newStatus == CourseStatus.CLOSED) {
    // // When closing from FULL, close without prompting (for non-interactive
    // // scenarios)
    // closeWithRandomWaitlistSelection(capacity);
    // } else if (newStatus == CourseStatus.CANCELLED) {
    // cancelCourse();
    // } else {
    // System.out.println(
    // "Invalid transition from FULL to " + newStatus + " (FULL->OPEN is automatic
    // on drop)");
    // }
    // break;
    // case CLOSED:
    // if (newStatus == CourseStatus.OPEN) {
    // status = CourseStatus.OPEN;
    // System.out.println(code + " transitioned CLOSED -> OPEN");
    // } else if (newStatus == CourseStatus.DRAFT) {
    // status = CourseStatus.DRAFT;
    // System.out.println(code + " transitioned CLOSED -> DRAFT");
    // } else if (newStatus == CourseStatus.CANCELLED) {
    // cancelCourse();
    // } else {
    // System.out.println("Invalid transition from CLOSED to " + newStatus);
    // }
    // break;
    // case CANCELLED:
    // // CANCELLED can now transition back to DRAFT
    // if (newStatus == CourseStatus.DRAFT) {
    // status = CourseStatus.DRAFT;
    // System.out.println(code + " transitioned CANCELLED -> DRAFT (reinstating
    // course)");
    // } else {
    // System.out.println("Invalid: CANCELLED can only transition to DRAFT for " +
    // code);
    // }
    // break;
    // default:
    // System.out.println("Unknown current status.");
    // }
    // }

    public void setStatusAdmin(CourseStatus newStatus) {
        state.setStatus(this, newStatus);
    }

    // Interactive version for admin with Scanner (prompts for capacity increase)
    // public void setStatusAdminInteractive(CourseStatus newStatus, Scanner
    // scanner) {
    // if (newStatus == null)
    // return;
    // if (newStatus == status) {
    // System.out.println("No change: " + code + " already " + status);
    // return;
    // }

    // // Special handling for FULL -> CLOSED with interactive prompt
    // if (status == CourseStatus.FULL && newStatus == CourseStatus.CLOSED) {
    // if (!waitlist.isEmpty()) {
    // System.out.println(code + " has " + waitlist.size() + " student(s) on
    // waitlist.");
    // System.out.print(
    // "Do you want to increase capacity before closing? (Enter new capacity, or 0
    // to not increase): ");
    // try {
    // int newCapacity = Integer.parseInt(scanner.nextLine().trim());
    // if (newCapacity > 0) {
    // if (newCapacity > capacity) {
    // capacity = newCapacity;
    // System.out.println("Capacity increased to " + newCapacity);
    // closeWithRandomWaitlistSelection(newCapacity);
    // } else {
    // System.out.println("New capacity must be greater than current capacity (" +
    // capacity
    // + "). No change.");
    // closeWithRandomWaitlistSelection(capacity);
    // }
    // } else {
    // System.out.println("No capacity increase.");
    // closeWithRandomWaitlistSelection(capacity);
    // }
    // } catch (NumberFormatException e) {
    // System.out.println("Invalid input. Closing without capacity increase.");
    // closeWithRandomWaitlistSelection(capacity);
    // }
    // } else {
    // // No waitlist, just close
    // closeWithRandomWaitlistSelection(capacity);
    // }
    // return;
    // }

    // // For all other transitions, use the standard method
    // setStatusAdmin(newStatus);
    // }

    public void setStatusAdminInteractive(CourseStatus newStatus, Scanner scanner) {
        if (getStatus() == CourseStatus.FULL && newStatus == CourseStatus.CLOSED && !waitlist.isEmpty()) {
            System.out.print("Increase capacity before closing? (Enter new cap, or 0): ");
            try {
                int newCap = Integer.parseInt(scanner.nextLine());
                if (newCap > capacity)
                    performCloseWithWaitlist(newCap);
                else
                    performCloseWithWaitlist(capacity);
            } catch (Exception e) {
                performCloseWithWaitlist(capacity);
            }
        } else {
            setStatusAdmin(newStatus);
        }
    }

    protected void performCancellation() {
        setState(new CancelledState());
        List<Student> toNotify = new ArrayList<>(enrolled);
        toNotify.addAll(waitlist);
        enrolled.clear();
        waitlist.clear();
        mediator.notifyCancellation(this, toNotify);
        System.out.println(code + " has been CANCELLED. All students dropped and waitlist cleared.");
    }

    // private void cancelCourse() {
    // status = CourseStatus.CANCELLED;
    // // clear enrolled and waitlist, update students
    // for (Student s : new ArrayList<>(enrolled)) {
    // s.removeCourseDirect(this);
    // }
    // for (Student s : new ArrayList<>(waitlist)) {
    // s.removeCourseDirect(this);
    // }
    // enrolled.clear();
    // waitlist.clear();
    // System.out.println(code + " has been CANCELLED. All students dropped and
    // waitlist cleared.");
    // }

    private void closeWithRandomWaitlistSelection(int targetCapacity) {
        status = CourseStatus.CLOSED;
        System.out.println(code + " transitioned FULL -> CLOSED");

        // If there are waitlisted students and space available, promote random students
        if (!waitlist.isEmpty()) {
            int availableSlots = targetCapacity - enrolled.size();
            if (availableSlots > 0) {
                Random random = new Random();
                List<Student> waitlistCopy = new ArrayList<>(waitlist);
                int promotionCount = Math.min(availableSlots, waitlistCopy.size());

                System.out.println("Randomly selecting " + promotionCount + " student(s) from waitlist:");
                for (int i = 0; i < promotionCount; i++) {
                    int randomIndex = random.nextInt(waitlistCopy.size());
                    Student promoted = waitlistCopy.remove(randomIndex);
                    waitlist.remove(promoted);
                    enrolled.add(promoted);
                    promoted.addEnrolledCourseDirect(this);
                    System.out.println("  Randomly selected: " + promoted.name + " for " + code);
                }
            }
        }
    }

    protected void performCloseWithWaitlist(int targetCap) {
        this.capacity = targetCap;
        setState(new ClosedState());
        System.out.println(code + " transitioned FULL -> CLOSED");
        if (!waitlist.isEmpty()) {
            int available = capacity - enrolled.size();
            if (available > 0) {
                Random rand = new Random();
                List<Student> copy = new ArrayList<>(waitlist);
                int count = Math.min(available, copy.size());
                for (int i = 0; i < count; i++) {
                    Student p = copy.remove(rand.nextInt(copy.size()));
                    waitlist.remove(p);
                    enrolled.add(p);
                    mediator.syncPromotion(p, this);
                    System.out.println("  Randomly selected: " + p.name + " for " + code);
                }
            }
        }
    }

    public void printRoster() {
        System.out.println("Roster for " + code + " - " + title + " (" + status + ", cap=" + capacity + "):");
        if (enrolled.isEmpty()) {
            System.out.println("  [no enrolled]");
        } else {
            for (Student s : enrolled) {
                System.out.println("  " + s.id + " - " + s.name);
            }
        }
    }

    public void printWaitlist() {
        System.out.println("Waitlist for " + code + ":");
        if (waitlist.isEmpty()) {
            System.out.println("  [no waitlisted]");
        } else {
            for (Student s : waitlist) {
                System.out.println("  " + s.id + " - " + s.name);
            }
        }
    }

    // Exposed getters for UI/reporting
    public int getCapacity() {
        return capacity;
    }

    public List<Student> getEnrolled() {
        return enrolled;
    }

    public LinkedList<Student> getWaitlist() {
        return waitlist;
    }

    public int getEnrolledCount() {
        return enrolled.size();
    }

    public int getWaitlistCount() {
        return waitlist.size();
    }
}
