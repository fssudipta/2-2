import java.util.*;

public class EduLearnPlatformDemo {

    // ================= ANSI COLOR CODES =================
    public static final String RESET = "\u001B[0m";

    public static final String BLACK = "\u001B[30m";
    public static final String RED = "\u001B[31m";
    public static final String GREEN = "\u001B[32m";
    public static final String YELLOW = "\u001B[33m";
    public static final String BLUE = "\u001B[34m";
    public static final String PURPLE = "\u001B[35m";
    public static final String CYAN = "\u001B[36m";
    public static final String WHITE = "\u001B[37m";
    public static final String BOLD = "\033[0;1m";

    private static Scanner scanner = new Scanner(System.in);
    private static ShoppingCart cart = new ShoppingCart("My Learning Cart");
    private static Checkout checkout = new Checkout();

    public static void main(String[] args) {
        boolean running = true;
        printWelcomeBanner();
        while (running) {
            printMainMenu();
            String choice = scanner.nextLine();
            switch (choice) {
                case "1":
                    addItemsToCart();
                    break;
                case "2":
                    applyAddonsToItems();
                    break;
                case "3":
                    viewCart();
                    break;
                case "4":
                    processCheckout();
                    running = false;
                    break;
                case "5":
                    running = false;
                    System.out.println(RED + BOLD + "\nExiting EduLearn Platform..." + RESET);
                    break;
                default:
                    System.out.println(RED + "!! Invalid choice. Please try again !!" + RESET);
            }
        }
    }

    private static void printWelcomeBanner() {
        System.out.println(BLUE + BOLD);
        System.out.println("==============================================================");
        System.out.println("                 EDULEARN PLATFORM CLI");
        System.out.println("==============================================================");
        System.out.println(RESET);
    }

    private static void printMainMenu() {
        System.out.println(CYAN + "\n---------------------- MAIN MENU ----------------------" + RESET);
        System.out.println(GREEN + "1." + RESET + " Add Course/Module to Cart");
        System.out.println(GREEN + "2." + RESET + " Add Optional Add-ons (Practice/Mentor)");
        System.out.println(GREEN + "3." + RESET + " View Current Cart");
        System.out.println(GREEN + "4." + RESET + " Checkout & Apply Discounts");
        System.out.println(GREEN + "5." + RESET + " Exit");
        System.out.print(YELLOW + "\nSelect an option: " + RESET);
    }

    private static void addItemsToCart() {
        System.out.println(PURPLE + "\n================ AVAILABLE CATALOG ================" + RESET);

        System.out.println("1. [Module] Full-Stack Web Development " + GREEN + "($20 base + Courses)" + RESET);
        System.out.println("2. [Module] Data Science Mastery " + GREEN + "($25 base + Courses)" + RESET);
        System.out.println("3. [Course] Individual Java Programming " + GREEN + "($50)" + RESET);
        System.out.println("4. [Lesson] Standalone Intro to Python " + GREEN + "($15, 2.0 hrs)" + RESET);

        System.out.print(YELLOW + "\nEnter choice: " + RESET);
        String choice = scanner.nextLine();

        switch (choice) {
            case "1":
                cart.addItem(createWebDevelopmentModule());
                System.out.println(GREEN + ">> Web Development Module added successfully." + RESET);
                break;
            case "2":
                cart.addItem(createDataScienceModule());
                System.out.println(GREEN + ">> Data Science Module added successfully." + RESET);
                break;
            case "3":
                cart.addItem(createJavaCourse());
                System.out.println(GREEN + ">> Java Programming Course added successfully." + RESET);
                break;
            case "4":
                cart.addItem(new Lesson("Intro to Python", 2.0, 15.0));
                System.out.println(GREEN + ">> Python Lesson added successfully." + RESET);
                break;
            default:
                System.out.println(RED + "!! Invalid catalog selection !!" + RESET);
        }
    }

    private static void applyAddonsToItems() {

        if (cart.isEmpty()) {
            System.out.println(RED + "\nCart is empty. Add items first." + RESET);
            return;
        }

        System.out.println(PURPLE + "\n============= ADD OPTIONAL SERVICES (MODULE ONLY) =============" + RESET);

        List<PurchaseableItem> items = cart.getItems();

        for (int i = 0; i < items.size(); i++) {
            PurchaseableItem item = items.get(i);
            String type = (item instanceof Module) ? "[Module]" : (item instanceof Course) ? "[Course]" : "[Lesson]";
            System.out.println((i + 1) + ". " + CYAN + type + " " + item.getName() + RESET);
        }

        try {
            System.out.print(YELLOW + "\nEnter item number: " + RESET);
            int itemIdx = Integer.parseInt(scanner.nextLine()) - 1;

            if (itemIdx < 0 || itemIdx >= items.size()) {
                System.out.println(RED + "Invalid item selection." + RESET);
                return;
            }

            PurchaseableItem selectedItem = items.get(itemIdx);

            if (!(selectedItem instanceof Module)) {
                System.out.println(RED + "\nAdd-ons can ONLY be applied to Modules!" + RESET);
                return;
            }

            System.out.println("\n1. Practice Question Set " + GREEN + "($10)" + RESET);
            System.out.println("2. Live Mentor Support " + GREEN + "($20)" + RESET);
            System.out.print(YELLOW + "Choice: " + RESET);

            String addonChoice = scanner.nextLine();

            cart.removeItem(selectedItem);

            if (addonChoice.equals("1")) {
                cart.addItem(new PracticeSetAddon(selectedItem));
                System.out.println(GREEN + ">> Practice Set successfully attached to Module." + RESET);
            } else if (addonChoice.equals("2")) {
                cart.addItem(new LiveMentorSupportAddon(selectedItem));
                System.out.println(GREEN + ">> Live Mentor Support activated for Module." + RESET);
            } else {
                cart.addItem(selectedItem);
                System.out.println(RED + "Invalid selection." + RESET);
            }

        } catch (Exception e) {
            System.out.println(RED + "Error: Please enter a valid number." + RESET);
        }
    }

    private static void viewCart() {
        if (cart.isEmpty()) {
            System.out.println(RED + "\nYour cart is currently empty." + RESET);
        } else {
            System.out.println(BLUE + "\n================ CURRENT CART DETAILS ================" + RESET);
            System.out.println(cart.getDetails(0));
        }
    }

    private static void processCheckout() {
        if (cart.isEmpty()) {
            System.out.println(RED + "Cannot checkout an empty cart." + RESET);
            return;
        }
        PurchaseableItem finalOrder = cart;
        int moduleCount = cart.getModuleCount();
        finalOrder = new MultiModuleDiscount(finalOrder, moduleCount);
        finalOrder = new SpecialDiscount(finalOrder);

        System.out.print(YELLOW + "\nAre you from a developing country? (yes/no): " + RESET);
        String answer = scanner.nextLine().trim().toLowerCase();
        if (answer.equals("yes")) {
            finalOrder = new DevelopingCountryDiscount(finalOrder);
        }

        System.out.println(CYAN + "\nProcessing Secure Payment..." + RESET);
        System.out.println(GREEN + checkout.generateReceipt(finalOrder) + RESET);
    }

    private static Course createJavaCourse() {
        Course course = new Course("Complete Java Programming", 50.0);
        course.addLesson(new Lesson("Intro", 2.0, 25.0));
        course.addLesson(new Lesson("OOP", 3.0, 35.0));
        return course;
    }

    private static Module createWebDevelopmentModule() {
        Module module = new Module("Full-Stack Web Dev", 20.0);
        Course c = new Course("Web Basics", 30.0);
        c.addLesson(new Lesson("HTML/CSS", 3.0, 40.0));
        module.addCourse(c);
        return module;
    }

    private static Module createDataScienceModule() {
        Module module = new Module("Data Science Mastery", 25.0);
        Course c = new Course("Python DS", 40.0);
        c.addLesson(new Lesson("Data Viz", 4.0, 50.0));
        module.addCourse(c);
        return module;
    }
}