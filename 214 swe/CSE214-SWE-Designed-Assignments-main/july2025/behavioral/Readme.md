# University Course Registration System

This is a console-based Java application (no external libraries) for a university course registration system. The code is intentionally designed with certain structural issues to help students learn about better design approaches through refactoring.

- All classes are in the default package and same directory.

## Files

- `CourseStatus.java`: Enum with five states: `DRAFT`, `OPEN`, `FULL`, `CLOSED`, `CANCELLED`.
- `Student.java`: Student model with direct method calls into `Course` (`enrollIn`, `waitlistFor`, `dropCourse`). Maintains `enrolledCourses` and `waitlistedCourses` lists. Course can also directly modify Student's lists.
- `Course.java`: Core logic with extensive `switch/if` checks on `CourseStatus` for every operation. Handles enrollment, waitlisting, dropping, capacity changes, admin status transitions, roster/waitlist printing. Directly manipulates Student objects (e.g., when promoting from waitlist). When closing a FULL course with waitlist, prompts admin to optionally increase capacity and randomly selects students.
- `RegistrarSystem.java`: Simple registry storing maps of all students and courses. Provides getter methods for lookups only—does not coordinate operations.
- `ConsoleUI.java`: Console interface with Student and Admin modes using `Scanner`. Directly calls methods on `Student` and `Course` objects.
- `Main.java`: Seeds 20 students and 7 courses with various initial states, performs sample operations, and launches the interactive UI.
- `TestScenarios.java`: Comprehensive automated test suite with 25 tests demonstrating all state transitions, enrollment flows, and cross-object interactions.

## Course State Transitions

The system manages five course states with specific transition rules:

### States

1. **DRAFT** - Course is being planned; not visible to students
2. **OPEN** - Students can enroll if seats available
3. **FULL** - Capacity reached; enrollment closed but waitlist open
4. **CLOSED** - Neither enrollment nor waitlist allowed
5. **CANCELLED** - Course cancelled; all students dropped, limited operations allowed

### Automatic Transitions

- **OPEN → FULL**: Triggered automatically when enrolled count reaches capacity
- **FULL → OPEN**: Triggered automatically when a student drops and seats become available

### Admin-Controlled Transitions

**From DRAFT:**

- DRAFT → OPEN ✓
- DRAFT → CLOSED ✓
- DRAFT → CANCELLED ✓

**From OPEN:**

- OPEN → CLOSED ✓
- OPEN → DRAFT ✓
- OPEN → CANCELLED ✓

**From FULL:**

- FULL → CLOSED ✓ (admin prompted to optionally increase capacity; if yes, random students selected from waitlist)
- FULL → CANCELLED ✓

**From CLOSED:**

- CLOSED → OPEN ✓
- CLOSED → DRAFT ✓
- CLOSED → CANCELLED ✓

**From CANCELLED:**

- CANCELLED → DRAFT ✓ (reinstating course for planning)

### Special Behaviors

**Waitlisting:**

- Only available when course is in FULL state
- Students on waitlist can be automatically promoted when spots open (FIFO during drops)
- When admin closes a FULL course with waitlist, admin is prompted to increase capacity

**Closing from FULL:**

- If waitlist is not empty, admin is prompted: "Enter new capacity, or 0 to not increase"
- If admin enters 0: course closes immediately, waitlist remains (but now inaccessible)
- If admin enters new capacity > current: capacity is increased, then random students from waitlist are promoted to fill available slots
- Random selection ensures fairness when multiple students are waiting
- Course then transitions to CLOSED state

### Transition Implementation

All transitions are currently implemented using `switch` statements and `if` conditionals in the `Course.setStatusAdmin()` method, which checks the current state and validates the requested transition. Invalid transitions print error messages.

## Design Issues to Consider

### Issue 1: Communication and Coordination Problems

Currently, the code exhibits scattered communication between objects:

**Observations:**

- `Student` directly calls `Course.tryEnroll()`, `Course.addToWaitlist()`, `Course.dropStudent()`
- `Course` directly calls `Student.addEnrolledCourseDirect()`, `Student.removeCourseDirect()`
- `ConsoleUI` directly calls both `Student` and `Course` methods
- When a student drops and someone is promoted from the waitlist, `Course` must update multiple `Student` objects directly
- Enrollment business logic is split between `Student` and `Course` classes
- Both `Student` and `Course` maintain duplicate state (lists of enrolled/waitlisted courses)
- No single place knows about or validates the complete enrollment operation

**Question:**
- What if `Someone who knows all` was responsible for coordinating all operations between `Student` and `Course`?


### Issue 2: Conditional Complexity for Course States

Currently, `Course` class contains extensive conditional logic based on `CourseStatus`:

**Observations:**

- `Course.tryEnroll()` has a large `switch` statement checking current status (OPEN, FULL, CLOSED, DRAFT, CANCELLED)
- `Course.addToWaitlist()` has conditional logic checking if state allows waitlisting (only FULL)
- `Course.setStatusAdmin()` has nested conditionals validating transitions from each state
- `Course.setCapacity()` needs to check status to decide how to respond
- `Course.closeWithRandomWaitlistSelection()` handles special logic for FULL→CLOSED transition
- Adding new states or changing transition rules requires modifying multiple methods
- The same status checks appear repeatedly across different methods
- Each method needs to know all possible states and their rules


**Question:**
- Could each course status have its own encapsulation that knows how to handle `tryEnroll()`, `addToWaitlist()`, `canTransitionTo()`, etc.?



## Compilation and Execution Instructions

### Interactive Mode

1. Compile: `javac *.java`
2. Run: `java Main`
3. Explore Student mode (add, drop, view schedule) and Admin mode (list courses, change status, set capacity, print roster/waitlist).

### Automated Test Scenarios

To see all state transitions and coordination issues demonstrated without manual interaction:

1. Compile: `javac *.java`
2. Run: `java TestScenarios`

The test suite is organized into 8 parts with 24 comprehensive tests:

**Part 1: Automatic State Transitions** (Tests 1-4)

- Automatic OPEN → FULL when enrollment reaches capacity
- FULL course behavior (rejects enrollment, accepts waitlist)
- Automatic FULL → OPEN on drop with waitlist promotion
- Multiple drops showing repeated automatic transitions

**Part 2: Admin State Transitions (Forward)** (Tests 5-10)

- DRAFT → OPEN (making course visible and enrollable)
- OPEN → CLOSED (fully closing the course)
- OPEN → DRAFT (reverting to draft state)
- FULL → CLOSED without waitlist
- FULL → CLOSED with random waitlist selection (capacity increased, random students promoted)
- DRAFT → CLOSED (closing before ever opening)

**Part 3: Admin State Transitions (Backward)** (Tests 11-12)

- CLOSED → OPEN (reopening a closed course)
- CLOSED → DRAFT (reverting to planning stage)

**Part 4: Capacity Changes Affecting State** (Tests 13-14)

- Capacity increase triggering FULL → OPEN
- Capacity decrease handling (over-capacity situations)

**Part 5: Course Cancellation** (Tests 15-18)

- Any state → CANCELLED (clears all rosters and waitlists)
- CANCELLED → DRAFT (reinstating cancelled course)
- CANCELLED → other states (invalid)
- Cancellation from FULL with waitlist

**Part 6: Invalid Transitions** (Tests 19-21)

- DRAFT → FULL (not allowed)
- FULL → OPEN manual attempt (automatic only)
- OPEN → FULL manual attempt (automatic only)

**Part 7: Tight Coupling Demonstration** (Tests 22-23)

- Student/Course cross-object manipulation
- Duplicate state maintenance in both objects
- Direct method calls between Student and Course

**Part 8: Registrar as Simple Lookup** (Test 24)

- Registrar provides only lookup functionality
- No coordination, validation, or notification
- UI and objects bypass Registrar for operations