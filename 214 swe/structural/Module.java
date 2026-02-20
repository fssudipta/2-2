import java.util.*;

public class Module implements PurchaseableItem {
    private String name;
    private double basePrice;
    private List<Course> courses;

    public Module(String name, double basePrice) {
        if (basePrice < 0)
            throw new IllegalArgumentException("Base price can't be negative.");
        this.name = name;
        this.basePrice = basePrice;
        this.courses = new ArrayList<>();
    }

    public void addCourse(Course course) {
        if (course == null)
            throw new IllegalArgumentException("Course can't be null.");
        courses.add(course);
    }

    public void removeCourse(Course course) {
        courses.remove(course);
    }

    public List<Course> getCourses() {
        return new ArrayList<>(courses);
    }

    @Override
    public double calculatePrice() {
        double totaLCoursePrice = 0;
        for (Course course : courses) {
            totaLCoursePrice += course.calculatePrice();
        }
        return basePrice + totaLCoursePrice;
    }

    @Override
    public double getDuration() {
        double totalDuration = 0;
        for (Course course : courses) {
            totalDuration += course.getDuration();
        }
        return totalDuration;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public String getDetails(int indent) {
        String indentation = "  ".repeat(indent);
        StringBuilder sb = new StringBuilder();
        sb.append(String.format("%sModule: %s (Duration: %.2f hrs, Price: $%.2f)%n",
                indentation, name, getDuration(), calculatePrice()));

        for (Course course : courses) {
            sb.append(course.getDetails(indent + 1)).append("\n");
        }

        return sb.toString().trim();
    }

    @Override
    public String toString() {
        return getDetails(0);
    }
}