import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SampleController {

    /**
     * Returns a simple greeting message.
     */
    @GetMapping("/hello")
    public String helloWorld() {
        return "Hello, World!";
    }

    /**
     * Returns details for a specific item by ID.
     */
    @GetMapping("/items/{itemId}")
    public Item getItem(@PathVariable int itemId) {
        return new Item(itemId, "Sample Item");
    }

    public static class Item {
        private int id;
        private String name;

        public Item(int id, String name) {
            this.id = id;
            this.name = name;
        }
        public int getId() { return id; }
        public String getName() { return name; }
    }
}
