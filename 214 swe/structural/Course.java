import java.util.*;

public class Course implements PurchaseableItem {
    private String name;
    private double basePrice;
    private List<Lesson> lessons;

    public Course(String name, double basePrice) {
        if (basePrice < 0)
            throw new IllegalArgumentException("Price can't be negative.");
        this.name = name;
        this.basePrice = basePrice;
        this.lessons = new ArrayList<>();
    }

    public void addLesson(Lesson lesson) {
        if (lesson == null)
            throw new IllegalArgumentException("Lesson can't be null.");
        lessons.add(lesson);
    }

    public void removeLesson(Lesson lesson) {
        lessons.remove(lesson);
    }

    public List<Lesson> getLessons() {
        return new ArrayList<>(lessons);
    }

    @Override
    public double calculatePrice() {
        double totalLessonPrice = 0;
        for (Lesson lesson : lessons) {
            totalLessonPrice += lesson.calculatePrice();
        }
        return basePrice + totalLessonPrice;
    }

    @Override
    public double getDuration() {
        double totalDuration = 0;
        for (Lesson lesson : lessons) {
            totalDuration += lesson.getDuration();
        }
        return totalDuration;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public String getDetails(int indent) {
        String indentation = " ".repeat(indent);
        StringBuilder sb = new StringBuilder();
        sb.append(String.format("%sCourse: %s (Duration: %.2f hrs, Price: $%.2f)%n",
                indentation, name, getDuration(), calculatePrice()));
        for (Lesson lesson : lessons) {
            sb.append(lesson.getDetails(indent + 1)).append("\n");
        }

        return sb.toString().trim();
    }

    @Override
    public String toString(){
        return getDetails(0);
    }
}
