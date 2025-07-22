import pygame


class OptionsSave:
    def __init__(self):
        self.languages = {"English" : {"play" : "Play", "options" : "Options", "quit" : "Quit", "back" : "Back", "language" : "Langauge:", "difficulty" : "Difficulty:", "normal" : "Normal", "easy" : "Easy", "hard" : "Hard", "continue" : "Continue", "finish" : "Finish", "fullscreen" : "Fullscreen:", "on" : "On", "off" : "Off", "game over" : "Game over", "victory" : "Victory", "credits" : "Credits", "game" : "Game", "controls" : "Controls", "up" : "Up:", "down" : "Down:", "left" : "Left:", "right" : "Right:", "press" : "Press the button", "end" : "Level end:", "players" : "Choose your ship", "create" : "Create new ship", "delete" : "Delete ship", "ship name" : "Ship's name:", "create2" : "Create", "bad name" : "Incorrect name!", "max ships" : "You have 6 ships!", "cancel" : "Cancel", "start" : "Start"},
                          "Magyar" : {"play" : "Játék", "options" : "Beállítások", "quit" : "Kilépés", "back" : "Vissza", "language" : "Nyelv:", "difficulty" : "Nehézség:", "normal" : "Normál", "easy" : "Könnyű", "hard" : "Nehéz", "continue" : "Folytatás", "finish" : "Befejezés", "fullscreen": "Teljes képernyő:", "on" : "Be", "off" : "Ki", "game over" : "Vége a játéknak", "victory" : "Győzelem", "credits" : "Készítők", "game" : "Játék", "controls" : "Irányítások", "up" : "Fel:", "down" : "Le:", "left" : "Bal:", "right" : "Jobb:", "press" : "Nyomd meg a gombot", "end" : "Szint vége:", "players" : "Válaszd ki a hajódat", "create" : "Új hajó létrehozása", "delete" : "Hajó törlése", "ship name" : "Hajó neve:", "create2" : "Létrehozás", "bad name" : "Helytelen név!", "max ships" : "6 hajód van!", "cancel" : "Mégsem", "start" : "Kezdés"}}
        self.select_language = "English"
        self.how_number = 0
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
            self.fullscreen = f.readline()
            self.fullscreen = self.fullscreen.strip("\n")
            if self.fullscreen == "True":
                self.fullscreen = True
            else:
                self.fullscreen = False
            self.up_control = int(f.readline().strip("\n"))
            self.down_control = int(f.readline().strip("\n"))
            self.left_control = int(f.readline().strip("\n"))
            self.right_control = int(f.readline().strip("\n"))

    def saving_writing(self):
        with (open("texts/options_saving", "w") as f):
            f.write(f"{self.select_language}\n")
            f.write(f"{str(self.how_number)}\n")
            f.write(f"{str(self.fullscreen)}\n")
            f.write(f"{str(self.up_control)}\n")
            f.write(f"{str(self.down_control)}\n")
            f.write(f"{str(self.left_control)}\n")
            f.write(f"{str(self.right_control)}\n")
