import java.util.*;

// the common interface for everything
interface FileSystemItem{
    String getName();
    int getSize();
    void showDetails();
}

// the leaf: a single file
class File implements FileSystemItem{
    private String name;
    private int size;
    public File(String name, int size){
        this.name=name;
        this.size=size;
    }
    @Override
    public String getName(){
        return name;
    }
    @Override
    public int getSize(){
        return size;
    }
    @Override
    public void showDetails(){
        System.out.println("File: "+name+" ("+size+"KB)");
    }
}

// The Composite: A folder that can contain files or other folders
class Folder implements FileSystemItem {
    private String name;
    private List<FileSystemItem> items = new ArrayList<>();

    public Folder(String name) {
        this.name = name;
    }

    public void add(FileSystemItem item) {
        items.add(item);
    }

    public void remove(FileSystemItem item) {
        items.remove(item);
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public int getSize() {
        int totalSize = 0;
        // recursively ask every child for its size
        for (FileSystemItem item : items) {
            totalSize += item.getSize();
        }
        return totalSize;
    }

    @Override
    public void showDetails() {
        System.out.println("Folder: " + name);
        for (FileSystemItem item : items) {
            System.out.print("  ");
            item.showDetails(); // recursively call children
        }
    }
}

public class FileSystemDemo {
    public static void main(String[] args) {
        // 1. Create individual files (Leaves)
        File file1 = new File("Resume.pdf", 50);
        File file2 = new File("Photo.jpg", 200);
        File file3 = new File("Notes.txt", 10);

        // 2. Create folders (Composites)
        Folder documents = new Folder("Documents");
        Folder images = new Folder("Images");
        Folder root = new Folder("Root");

        // 3. Build the tree structure
        documents.add(file1);
        documents.add(file3);

        images.add(file2);

        root.add(documents);
        root.add(images);

        // 4. Treat them uniformly!
        System.out.println("--- Getting Sizes ---");
        // We call getSize() on a File...
        System.out.println(file1.getName() + " size: " + file1.getSize() + "KB");
        
        // ...and we call getSize() on a Folder (which calculates total internally)
        System.out.println(documents.getName() + " size: " + documents.getSize() + "KB");
        System.out.println(root.getName() + " size: " + root.getSize() + "KB");

        System.out.println("\n--- Showing Details ---");
        // We call showDetails() on the root, and it prints everything
        root.showDetails();
    }
}