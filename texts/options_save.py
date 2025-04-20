import pygame


class OptionsSave:
    def __init__(self):
        self.languages = {"English" : {"play" : "Play", "options" : "Options", "quit" : "Quit", "back" : "Back", "language" : "Langauge:", "difficulty" : "Difficulty:", "normal" : "Normal", "easy" : "Easy", "hard" : "Hard", "continue" : "Continue", "finish" : "Finish", "fullscreen" : "Fullscreen:", "on" : "On", "off" : "Off", "game over" : "Game over", "victory" : "Victory", "credits" : "Credits", "game" : "Game", "controls" : "Controls", "up" : "Up:", "down" : "Down:", "left" : "Left:", "right" : "Right:", "press" : "Press the button"},
                          "Magyar" : {"play" : "Játék", "options" : "Beállítások", "quit" : "Kilépés", "back" : "Vissza", "language" : "Nyelv:", "difficulty" : "Nehézség:", "normal" : "Normál", "easy" : "Könnyű", "hard" : "Nehéz", "continue" : "Folytatás", "finish" : "Befejezés", "fullscreen": "Teljes képernyő:", "on" : "Be", "off" : "Ki", "game over" : "Vége a játéknak", "victory" : "Győzelem", "credits" : "Készítők", "game" : "Játék", "controls" : "Irányítások", "up" : "Fel:", "down" : "Le:", "left" : "Bal:", "right" : "Jobb:", "press" : "Nyomd meg a gombot"}}
        self.select_language = "English"
        self.how_number = 0
        self.game_difficulty = 0
        self.fullscreen = True
        self.up_control = pygame.K_w
        self.down_control = pygame.K_s
        self.left_control = pygame.K_a
        self.right_control = pygame.K_d
        self.saving_reading()

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
            self.fullscreen = f.readline()
            self.fullscreen = self.fullscreen.strip("\n")
            if self.fullscreen == "True":
                self.fullscreen = True
            else:
                self.fullscreen = False

    def saving_writing(self):
        with (open("texts/options_saving", "w") as f):
            f.write(f"{self.select_language}\n")
            f.write(f"{str(self.how_number)}\n")
            f.write(f"{str(self.game_difficulty)}\n")
            f.write(f"{str(self.fullscreen)}\n")
