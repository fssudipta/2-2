// 1. The Abstract Class (The "Template")
abstract class DataMiner {
    // The Template Method: Final so the structure can't be changed
    public final void mineData() {
        openFile();
        extractData(); // Subclasses decide how
        closeFile();
    }
    private void openFile() { System.out.println("Opening file..."); }
    private void closeFile() { System.out.println("Closing file..."); }
    
    protected abstract void extractData(); // The "hook" for subclasses
}

// 2. Concrete Implementation
class PDFMiner extends DataMiner {
    protected void extractData() { System.out.println("Extracting PDF text..."); }
}

// 3. The Client (Main)
public class TemplateMain {
    public static void main(String[] args) {
        DataMiner miner = new PDFMiner();
        miner.mineData(); // Client calls the template, not the individual steps
    }
}