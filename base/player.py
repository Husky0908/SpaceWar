import pygame


class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.health = 5
        self.width = 20
        self.height = 40
        self.form = None
        self.pictures = [pygame.image.load("Pictures/players_pictures/player_ship_1_hp_j.png").convert_alpha(), pygame.image.load(
            "Pictures/players_pictures/player_ship_2_hp_j.png").convert_alpha(), pygame.image.load(
            "Pictures/players_pictures/player_ship_3_hp_j.png").convert_alpha(), pygame.image.load(
            "Pictures/players_pictures/player_ship_4_hp_j.png").convert_alpha(), pygame.image.load(
            "Pictures/players_pictures/player_ship_5_hp_j.png").convert_alpha()]
        self.r = None

