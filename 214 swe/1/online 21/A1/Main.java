// The Product Interface
interface DocumentProcessor {
    void loadDocument(String fileName);

    void saveDocument(String fileName);
}

// Concrete Products
class DocxProcessor implements DocumentProcessor {
    public void loadDocument(String fileName) {
        System.out.println("Loading .docx file: " + fileName);
    }

    public void saveDocument(String fileName) {
        System.out.println("Saving .docx file: " + fileName);
    }
}

class PdfProcessor implements DocumentProcessor {
    public void loadDocument(String fileName) {
        System.out.println("Loading .pdf file: " + fileName);
    }

    public void saveDocument(String fileName) {
        System.out.println("Saving .pdf file: " + fileName);
    }
}

class TxtProcessor implements DocumentProcessor {
    public void loadDocument(String fileName) {
        System.out.println("Loading .txt file: " + fileName);
    }

    public void saveDocument(String fileName) {
        System.out.println("Saving .txt file: " + fileName);
    }
}

// Factory
class DocumentProcessorFactory {
    public static DocumentProcessor getProcessor(String fileName) {
        if (fileName.endsWith(".docx")) {
            return new DocxProcessor();
        } else if (fileName.endsWith(".pdf")) {
            return new PdfProcessor();
        } else if (fileName.endsWith(".txt")) {
            return new TxtProcessor();
        } else {
            throw new IllegalArgumentException("Unsupported file format.");
        }
    }
}

// Client Code
public class Main {
    public static void main(String[] args) {
        // Example inputs
        String[] files = { "report.docx", "manual.pdf", "notes.txt" };

        for (String file : files) {
            try {
                DocumentProcessor processor = DocumentProcessorFactory.getProcessor(file);

                processor.loadDocument(file);
                processor.saveDocument(file);
                System.out.println("done");
            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        }
    }
}