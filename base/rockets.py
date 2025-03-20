import pygame


class Rocket:
    def __init__(self, x: int, y: int, attacker: str):
        self.x = x
        self.y = y
        self.health = 1
        self.dest_x = None
        self.dest_y = None
        self.dir_x = None
        self.dir_y = None
        self.speed = 3
        self.form = None
        self.r = 10
        self.attacker = attacker
        self.state = Rocket.STATE_MOVE
        self.time = 0

    height = 25
    width = 25

    STATE_MOVE = 1
    STATE_DESTROY = 2


class Rockets:
    def __init__(self):
        self.elements = []


    def spawn(self, x, y, attacker):
        self.elements.append(Rocket(x, y, attacker))
