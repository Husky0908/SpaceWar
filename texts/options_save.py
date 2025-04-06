from game.game_logic import GameLogic

class OptionsSave:
    def __init__(self):
        self.languages = {"English" : {"play" : "Play", "options" : "Options", "quit" : "Quit", "back" : "Back", "language" : "Langauge:", "difficulty" : "Difficulty:", "normal" : "Normal", "easy" : "Easy", "hard" : "Hard"},
                          "Magyar" : {"play" : "Játék", "options" : "Beállítások", "quit" : "Kilépés", "back" : "Vissza", "language" : "Nyelv:", "difficulty" : "Nehézség:", "normal" : "Normál", "easy" : "Könnyű", "hard" : "Nehéz"}}
        self.select_language = "English"
        self.how_number = 0
        self.game_difficulty = 0

    def saving_reading(self):
        with (open("texts/options_saving", "r") as f):
            self.select_language = f.readline()
            self.select_language = self.select_language.strip("\n")
            self.how_number = f.readline()
            self.how_number = self.how_number.strip("\n")
            self.how_number = int(self.how_number)
            self.game_difficulty = f.readline()
            self.game_difficulty = self.game_difficulty.strip("\n")
            self.game_difficulty = int(self.game_difficulty)

    def saving_writing(self):
        with (open("texts/options_saving", "w") as f):
            f.write(f"{self.select_language}\n")
            f.write(f"{str(self.how_number)}\n")
            f.write(f"{str(self.game_difficulty)}\n")
