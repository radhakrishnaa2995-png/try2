import random
import string

def clean_word(word):
    return "".join(ch for ch in word.upper() if ch.isalpha())

def make_word_search(words, size=12):
    grid = [["" for _ in range(size)] for _ in range(size)]
    directions = [(1,0), (0,1), (1,1), (-1,1)]
    placed = []

    for raw in words:
        word = clean_word(raw)
        if not word or len(word) > size:
            continue

        for _ in range(100):
            dx, dy = random.choice(directions)

            if dx == 1:
                x = random.randint(0, size - len(word))
            elif dx == -1:
                x = random.randint(len(word) - 1, size - 1)
            else:
                x = random.randint(0, size - 1)

            if dy == 1:
                y = random.randint(0, size - len(word))
            else:
                y = random.randint(0, size - 1)

            cells = []
            conflict = False

            for i, ch in enumerate(word):
                cx = x + dx * i
                cy = y + dy * i
                current = grid[cy][cx]

                if current not in ("", ch):
                    conflict = True
                    break

                cells.append((cx, cy, ch))

            if not conflict:
                for cx, cy, ch in cells:
                    grid[cy][cx] = ch
                placed.append(word)
                break

    for y in range(size):
        for x in range(size):
            if grid[y][x] == "":
                grid[y][x] = random.choice(string.ascii_uppercase)

    return grid, placed

def get_theme_data(theme):
    theme = theme.lower().strip()

    data = {
        "dinosaurs": {
            "words": ["Tyrannosaurus", "Triceratops", "Fossil", "Jurassic", "Raptor", "Stegosaurus", "Herbivore", "Carnivore", "Egg", "Volcano"],
            "trivia": [
                ("Which dinosaur is famous for its tiny arms?", "Tyrannosaurus Rex"),
                ("What do we call preserved dinosaur bones?", "Fossils"),
                ("Which dinosaur had three horns?", "Triceratops"),
                ("What kind of dinosaur eats plants?", "Herbivore"),
                ("What kind of dinosaur eats meat?", "Carnivore"),
                ("Which period is famous for many dinosaurs?", "Jurassic"),
                ("What do baby dinosaurs hatch from?", "Eggs"),
                ("Which dinosaur had plates on its back?", "Stegosaurus"),
            ],
            "clues": [
                ("Preserved dinosaur bones", "Fossil"),
                ("Three-horned dinosaur", "Triceratops"),
                ("Plant-eating animal", "Herbivore"),
                ("Meat-eating animal", "Carnivore"),
                ("Dinosaur baby home", "Egg"),
            ],
        },

        "space": {
            "words": ["Planet", "Rocket", "Astronaut", "Galaxy", "Moon", "Mars", "Orbit", "Comet", "Star", "Solar"],
            "trivia": [
                ("Which planet is known as the Red Planet?", "Mars"),
                ("What do astronauts ride into space?", "Rocket"),
                ("What is Earth’s natural satellite?", "Moon"),
                ("What is a huge group of stars called?", "Galaxy"),
                ("What path does a planet follow around the Sun?", "Orbit"),
                ("What bright object has a tail in space?", "Comet"),
            ],
            "clues": [
                ("Red Planet", "Mars"),
                ("Space traveler", "Astronaut"),
                ("Earth's natural satellite", "Moon"),
                ("Group of stars", "Galaxy"),
                ("Space vehicle", "Rocket"),
            ],
        },

        "animals": {
            "words": ["Lion", "Tiger", "Elephant", "Giraffe", "Zebra", "Monkey", "Penguin", "Dolphin", "Rabbit", "Parrot"],
            "trivia": [
                ("Which animal is known as the king of the jungle?", "Lion"),
                ("Which animal has a very long neck?", "Giraffe"),
                ("Which bird cannot fly and lives in cold places?", "Penguin"),
                ("Which sea animal is very intelligent and friendly?", "Dolphin"),
                ("Which animal has black and white stripes?", "Zebra"),
            ],
            "clues": [
                ("King of the jungle", "Lion"),
                ("Long-necked animal", "Giraffe"),
                ("Black and white striped animal", "Zebra"),
                ("Smart sea animal", "Dolphin"),
                ("Colorful talking bird", "Parrot"),
            ],
        }
    }

    return data.get(theme, data["dinosaurs"])
