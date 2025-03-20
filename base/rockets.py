from base.player import Player
from base.directions import get_direction


class Rocket:

    height = 25
    width = 25
    STATE_MOVE = 1
    STATE_DESTROY = 2

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

    def control(self, player: Player):
        if self.state == Rocket.STATE_MOVE:
            self.dest_x = player.x
            self.dest_y = player.y
            self.dir_x, self.dir_y = get_direction(self.x, self.y, self.dest_x, self.dest_y)
            self.x = self.x + self.dir_x * self.speed
            self.y = self.y + self.dir_y * self.speed
        if self.health <= 0:
            self.state = Rocket.STATE_DESTROY


    def contacts(self, player: Player):
            if self.form.colliderect(self.r):
                self.state = Rocket.STATE_DESTROY
                player.health = player.health - 1


class Rockets:
    def __init__(self):
        self.elements = []


    def spawn(self, x, y, attacker):
        self.elements.append(Rocket(x, y, attacker))


    def control(self, player: Player):
        for rocket in self.elements:
            rocket.control(player)
