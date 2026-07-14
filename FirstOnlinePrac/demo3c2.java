
class GameConfig {
    private static GameConfig instance;
    private int resolution;
    private int volume;
    private int level;

    GameConfig() {
        System.out.println("Instance created");
    }

    public static GameConfig getInstance() {
        if (instance == null) {
            instance = new GameConfig();
        }
        return instance;
    }

}

class AI {

}

public class demo3c2 {

    public static void main(String[] args) {

    }
}
