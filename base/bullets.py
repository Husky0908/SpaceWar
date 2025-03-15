import pygame


class Bullet:
    def __init__(self, x_0: int, y_0: int, destination_x: float, destination_y: float, attacker: str):
        self.x_0 = x_0
        self.y_0 = y_0
        self.x = x_0
        self.y = y_0
        self.dest_x = destination_x
        self.dest_y = destination_y
        self.dir_x = None
        self.dir_y = None
        self.speed = 400
        self.start_time = 0
        self.sharp = False
        self.form = None
        self.forms = [pygame.image.load("Pictures/players_pictures/player_bullet.png")]
        self.r = 10
        self.attacker = attacker


class Bullets:
    def __init__(self):
        self.last_spawn = 100
        self.elements = []
