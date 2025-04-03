class OptionsSave:
    def __init__(self):
        self.languages = {"English" : {"play" : "Play", "options" : "Options", "quit" : "Quit", "back" : "Back", "language" : "Langauge:"},
                          "Magyar" : {"play" : "Játék", "options" : "Beállítások", "quit" : "Kilépés", "back" : "Vissza", "language" : "Nyelv:"}}
        self.select_language = "English"
        self.how_number = 0

    def saving_reading(self):
        with (open("texts/options_saving", "r") as f):
            self.select_language = f.readline()
            self.select_language = self.select_language.strip("\n")
            self.how_number = f.readline()
            self.how_number = self.how_number.strip("\n")
            self.how_number = int(self.how_number)

    def saving_writing(self):
        with (open("texts/options_saving", "w") as f):
            f.write(f"{self.select_language}\n")
            f.write(f"{str(self.how_number)}\n")
