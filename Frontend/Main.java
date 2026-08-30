import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.Button;
import javafx.stage.Stage;

public class Main extends Application {
    @Override
    public void start(Stage stage) {
        Button button = new Button("Start Search");
        stage.setScene(new Scene(button, 400, 300));
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}
