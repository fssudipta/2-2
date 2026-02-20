
public class Test {

    public static void main(String[] args) {
        System.out.println("==============================================================");
        System.out.println("         EDULEARN PLATFORM - COMPREHENSIVE DEMO               ");
        System.out.println("==============================================================\n");

        testSingleLesson(); // Test 1: Single Lesson Purchase

        testSingleCourse(); // Test 2: Single Course Purchase

        testSingleModule(); // Test 3: Single Module Purchase

        testModuleWithPracticeSet(); // Test 4: Module with Practice Set Add-on

        testModuleWithMentorSupport(); // Test 5: Module with Live Mentor Support

        testModuleWithBothAddons(); // Test 6: Module with Both Add-ons

        testMultiModuleDiscount(); // Test 7: Multi-Module Discount (2 modules)

        testSpecialDiscount(); // Test 8: Special Discount (5+ hours duration)

        testDevelopingCountryDiscount(); // Test 9: Developing Country Student Discount

        testMultipleDiscounts(); // Test 10: Multiple Discounts Combined

        testComplexScenario();// Test 11: Complex Scenario-All Features

        testEdgeCases();// Test 12: Edge Cases

        System.out.println("==============================================================");
        System.out.println("                            DEMO                             ");
        System.out.println("==============================================================\n");
    }

    private static void testSingleLesson() {
        printTestHeader("Test 1: Single Lesson Purchase");

        Lesson lesson = new Lesson("Introduction to Java", 2.0, 25.0);
        Checkout checkout = new Checkout();
        System.out.println(checkout.generateReceipt(lesson));

        printSeparator();
    }

    private static void testSingleCourse() {
        printTestHeader("Test 2: Single Course Purchase");

        Course course = createJavaCourse();
        Checkout checkout = new Checkout();
        System.out.println(checkout.generateReceipt(course));

        printSeparator();
    }

    private static void testSingleModule() {
        printTestHeader("Test 3: Single Module Purchase");

        Module module = createWebDevelopmentModule();
        Checkout checkout = new Checkout();
        System.out.println(checkout.generateReceipt(module));

        printSeparator();
    }

    private static void testModuleWithPracticeSet() {
        printTestHeader("Test 4: Module with Practice Set Add-on");

        Module module = createWebDevelopmentModule();
        PurchaseableItem moduleWithPractice = new PracticeSetAddon(module);
        Checkout checkout = new Checkout();
        System.out.println(checkout.generateReceipt(moduleWithPractice));

        printSeparator();
    }

    private static void testModuleWithMentorSupport() {
        printTestHeader("Test 5: Module with Live Mentor Support");

        Module module = createWebDevelopmentModule();
        PurchaseableItem moduleWithMentor = new LiveMentorSupportAddon(module);
        Checkout checkout = new Checkout();
        System.out.println(checkout.generateReceipt(moduleWithMentor));

        printSeparator();
    }

    private static void testModuleWithBothAddons() {
        printTestHeader("Test 6: Module with Both Add-ons");

        Module module = createWebDevelopmentModule();
        PurchaseableItem moduleWithAddons = new LiveMentorSupportAddon(new PracticeSetAddon(module));
        Checkout checkout = new Checkout();
        System.out.println(checkout.generateReceipt(moduleWithAddons));

        printSeparator();
    }

    private static void testMultiModuleDiscount() {
        printTestHeader("Test 7: Multi-Module Discount (2 modules in cart)");

        ShoppingCart cart = new ShoppingCart();
        cart.addItem(createWebDevelopmentModule());
        cart.addItem(createDataScienceModule());

        int moduleCount = cart.getModuleCount();
        PurchaseableItem cartWithDiscount = new MultiModuleDiscount(cart, moduleCount);
        Checkout checkout = new Checkout();
        System.out.println(checkout.generateReceipt(cartWithDiscount));

        printSeparator();
    }

    private static void testSpecialDiscount() {
        printTestHeader("Test 8: Special Discount (Duration >= 5 hours)");

        Module module = createWebDevelopmentModule(); // This has 6 hours
        PurchaseableItem moduleWithDiscount = new SpecialDiscount(module);
        Checkout checkout = new Checkout();
        System.out.println(checkout.generateReceipt(moduleWithDiscount));

        printSeparator();
    }

    private static void testDevelopingCountryDiscount() {
        printTestHeader("Test 9: Developing Country Student Discount");

        Module module = createDataScienceModule();
        PurchaseableItem moduleWithDiscount = new DevelopingCountryDiscount(module);
        Checkout checkout = new Checkout();
        System.out.println(checkout.generateReceipt(moduleWithDiscount));

        printSeparator();
    }

    private static void testMultipleDiscounts() {
        printTestHeader("Test 10: Multiple Discounts Combined");
        System.out.println("Scenario: Developing country student buying module with");
        System.out.println("Practice Set (5+ hours duration for special discount)\n");

        Module module = createWebDevelopmentModule();

        PurchaseableItem withPractice = new PracticeSetAddon(module); // Add practice set addon
        PurchaseableItem withSpecialDiscount = new SpecialDiscount(withPractice); // Apply special discount (duration >=
                                                                                  // 5 hours)
        PurchaseableItem withAllDiscounts = new DevelopingCountryDiscount(withSpecialDiscount); // Apply developing
                                                                                                // country discount

        Checkout checkout = new Checkout();
        System.out.println(checkout.generateReceipt(withAllDiscounts));
        printSeparator();
    }

    private static void testComplexScenario() {
        printTestHeader("Test 11: Complex Scenario - All Features Combined");
        System.out.println("Scenario: Developing country student purchasing 2 modules");
        System.out.println("with Practice Sets and Mentor Support\n");

        Module webModule = createWebDevelopmentModule(); // Create first module with add-ons
        PurchaseableItem webWithAddons = new LiveMentorSupportAddon(new PracticeSetAddon(webModule));
        Module dataModule = createDataScienceModule(); // Create second module with add-ons
        PurchaseableItem dataWithAddons = new LiveMentorSupportAddon(new PracticeSetAddon(dataModule));

        ShoppingCart cart = new ShoppingCart("Premium Learning Package"); // Add to cart
        cart.addItem(webWithAddons);
        cart.addItem(dataWithAddons);

        PurchaseableItem withMultiModuleDiscount = new MultiModuleDiscount(cart, cart.getModuleCount()); // Apply
                                                                                                         // multi-module
                                                                                                         // discount
        PurchaseableItem withSpecialDiscount = new SpecialDiscount(withMultiModuleDiscount);
        PurchaseableItem finalPackage = new DevelopingCountryDiscount(withSpecialDiscount);

        Checkout checkout = new Checkout();
        System.out.println(checkout.generateReceipt(finalPackage));

        printSeparator();
    }

    private static void testEdgeCases() {
        printTestHeader("Test 12: Edge Cases");

        System.out.println("Edge Case 1: Single module (no multi-module discount)");
        ShoppingCart cart1 = new ShoppingCart();
        cart1.addItem(createWebDevelopmentModule());
        PurchaseableItem noDiscount = new MultiModuleDiscount(cart1, cart1.getModuleCount());
        System.out.printf("Price: $%.2f (discount not applied)%n%n", noDiscount.calculatePrice());

        System.out.println("Edge Case 2: Course with duration < 5 hours (no special discount)");
        Course shortCourse = new Course("Quick Python Intro", 30.0);
        shortCourse.addLesson(new Lesson("Python Basics", 2.0, 15.0));
        shortCourse.addLesson(new Lesson("Variables", 1.5, 10.0));
        PurchaseableItem noSpecialDiscount = new SpecialDiscount(shortCourse);
        System.out.printf("Duration: %.2f hrs, Price: $%.2f (discount not applied)%n%n",
                noSpecialDiscount.getDuration(), noSpecialDiscount.calculatePrice());

        System.out.println("Edge Case 3: Zero-priced item with discounts");
        Lesson freeLesson = new Lesson("Free Introduction", 1.0, 0.0);
        PurchaseableItem freeWithDiscount = new DevelopingCountryDiscount(freeLesson);
        System.out.printf("Price: $%.2f (cannot go below zero)%n%n",
                freeWithDiscount.calculatePrice());

        System.out.println("Edge Case 4: Empty shopping cart");
        ShoppingCart emptyCart = new ShoppingCart();
        System.out.printf("Empty cart - Items: %d, Price: $%.2f, Duration: %.2f hrs%n%n",
                emptyCart.size(), emptyCart.calculatePrice(), emptyCart.getDuration());

        System.out.println("Edge Case 5: Course with no lessons");
        Course emptyCourse = new Course("Future Course", 50.0);
        System.out.printf("Course with no lessons - Duration: %.2f hrs, Price: $%.2f%n%n",
                emptyCourse.getDuration(), emptyCourse.calculatePrice());

        System.out.println("Edge Case 6: Multiple discount layers");
        Module module = createWebDevelopmentModule();
        PurchaseableItem multiLayered = new DevelopingCountryDiscount(
                new SpecialDiscount(
                        new DevelopingCountryDiscount(
                                new SpecialDiscount(module))));
        System.out.printf("Multiple layers applied - Final Price: $%.2f%n",
                multiLayered.calculatePrice());
        System.out.println("(Each discount applied independently)\n");

        printSeparator();
    }

    private static Course createJavaCourse() {
        Course course = new Course("Complete Java Programming", 50.0);
        course.addLesson(new Lesson("Introduction to Java", 2.0, 25.0));
        course.addLesson(new Lesson("Object-Oriented Programming", 3.0, 35.0));
        course.addLesson(new Lesson("Collections Framework", 2.5, 30.0));
        return course;
    }

    private static Course createWebDevCourse() {
        Course course = new Course("Modern Web Development", 45.0);
        course.addLesson(new Lesson("HTML & CSS Fundamentals", 2.0, 20.0));
        course.addLesson(new Lesson("JavaScript Essentials", 2.5, 25.0));
        course.addLesson(new Lesson("React Framework", 3.0, 30.0));
        return course;
    }

    private static Module createWebDevelopmentModule() {
        Module module = new Module("Full-Stack Web Development", 20.0);
        module.addCourse(createJavaCourse());
        module.addCourse(createWebDevCourse());
        return module;
    }

    private static Course createPythonCourse() {
        Course course = new Course("Python for Data Science", 55.0);
        course.addLesson(new Lesson("Python Basics", 2.0, 20.0));
        course.addLesson(new Lesson("NumPy and Pandas", 3.0, 30.0));
        course.addLesson(new Lesson("Data Visualization", 2.5, 25.0));
        return course;
    }

    private static Course createMLCourse() {
        Course course = new Course("Machine Learning Fundamentals", 60.0);
        course.addLesson(new Lesson("Introduction to ML", 2.0, 25.0));
        course.addLesson(new Lesson("Supervised Learning", 3.5, 35.0));
        course.addLesson(new Lesson("Neural Networks", 3.0, 30.0));
        return course;
    }

    private static Module createDataScienceModule() {
        Module module = new Module("Data Science Mastery", 25.0);
        module.addCourse(createPythonCourse());
        module.addCourse(createMLCourse());
        return module;
    }

    private static void printTestHeader(String title) {
        System.out.println("\n" + "-".repeat(60));
        System.out.println("  " + title);
        System.out.println("-".repeat(60) + "\n");
    }

    private static void printSeparator() {
        System.out.println("\n" + "=".repeat(60) + "\n");
    }
}
