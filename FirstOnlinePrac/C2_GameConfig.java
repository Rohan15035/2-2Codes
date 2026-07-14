// ===================================================================
// C2 : Game-engine configuration manager  ->  SINGLETON PATTERN
// -------------------------------------------------------------------
// Settings are loaded from disk ONCE (expensive) and shared by every
// subsystem (Graphics, Audio, AI). Multiple copies could desync the
// game state, so only a single GameConfig instance may ever exist.
//   1. private static instance
//   2. private constructor (does the one-time disk load)
//   3. public static getInstance() as the only way to obtain it
// ===================================================================

class GameConfig {
    // 1. The single shared instance
    private static GameConfig instance;

    private String resolution;
    private int    audioVolume;
    private String difficulty;

    // 2. Private constructor: the "expensive" load happens exactly once
    private GameConfig() {
        System.out.println("Loading configuration from disk (expensive)...");
        this.resolution  = "1920x1080";
        this.audioVolume = 80;
        this.difficulty  = "Hard";
    }

    // 3. Global access point
    public static GameConfig getInstance() {
        if (instance == null) {
            instance = new GameConfig();
        }
        return instance;
    }

    public void printConfig() {
        System.out.println("Resolution=" + resolution
                + ", Volume=" + audioVolume
                + ", Difficulty=" + difficulty);
    }
}

public class C2_GameConfig {
    public static void main(String[] args) {
        // Three subsystems each "instantiate" the config...
        GameConfig graphics = GameConfig.getInstance();
        GameConfig audio    = GameConfig.getInstance();
        GameConfig ai       = GameConfig.getInstance();

        graphics.printConfig();

        // ...but all three references point to the SAME object.
        System.out.println("All subsystems share one instance? "
                + (graphics == audio && audio == ai));
    }
}
