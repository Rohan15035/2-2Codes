// ============================================================================
// Q6  (CSE 214 - C2)  Document generator
// Two modes: professional/formal and informal. In its chosen mode the client can
// create Letters and Resumes in the matching style. A document creator class must
// have functions that RETURN letter/resume objects.
//
// PATTERN : ABSTRACT FACTORY
//   DocumentCreator is the abstract factory with createLetter() and
//   createResume(). FormalDocumentCreator and InformalDocumentCreator are the two
//   concrete factories, each producing a consistent FAMILY of styled documents
//   (a formal creator never returns an informal resume).
//
// SOLID :
//   - DIP : the client depends on DocumentCreator / Letter / Resume abstractions.
//   - OCP : add a "Marketing" mode = one new factory + its products, no edits.
//   - LSP : either concrete creator works wherever DocumentCreator is expected.
//   - ISP : Letter and Resume are separate, focused product interfaces.
// ============================================================================

// ---------------- Abstract products ------------------------------------------
interface Letter { void render(); }
interface Resume { void render(); }

// ---------------- Formal family ----------------------------------------------
class FormalLetter implements Letter {
    public void render() { System.out.println("  [Letter] Dear Sir/Madam, ... Yours faithfully. (formal)"); }
}
class FormalResume implements Resume {
    public void render() { System.out.println("  [Resume] Objective | Experience | Education (serif, formal)"); }
}

// ---------------- Informal family --------------------------------------------
class InformalLetter implements Letter {
    public void render() { System.out.println("  [Letter] Hey! ... Catch you later :) (informal)"); }
}
class InformalResume implements Resume {
    public void render() { System.out.println("  [Resume] About me | Cool projects | Skills (colourful, informal)"); }
}

// ---------------- The Abstract Factory ---------------------------------------
interface DocumentCreator {
    String mode();
    Letter createLetter();
    Resume createResume();
}

// ---------------- Concrete factories -----------------------------------------
class FormalDocumentCreator implements DocumentCreator {
    public String mode()          { return "Professional/Formal"; }
    public Letter createLetter()  { return new FormalLetter(); }
    public Resume createResume()  { return new FormalResume(); }
}
class InformalDocumentCreator implements DocumentCreator {
    public String mode()          { return "Informal"; }
    public Letter createLetter()  { return new InformalLetter(); }
    public Resume createResume()  { return new InformalResume(); }
}

public class DocumentCreatorDemo {

    // Selects the factory for the client's preferred mode.
    static DocumentCreator creatorFor(String mode) {
        switch (mode.toLowerCase()) {
            case "formal": return new FormalDocumentCreator();
            case "informal": return new InformalDocumentCreator();
            default: throw new IllegalArgumentException("Unknown mode: " + mode);
        }
    }

    // Client code works only through the abstract creator.
    static void produceDocuments(String mode) {
        System.out.println("--- Mode selected: " + mode + " ---");
        try {
            DocumentCreator creator = creatorFor(mode);
            System.out.println("Using " + creator.mode() + " document creator:");
            creator.createLetter().render();
            creator.createResume().render();
        } catch (IllegalArgumentException ex) {
            System.out.println("  [Rejected] " + ex.getMessage());
        }
        System.out.println();
    }

    public static void main(String[] args) {
        produceDocuments("formal");
        produceDocuments("informal");
        produceDocuments("comic");   // boundary: unknown mode
    }
}
