import pygame
from base.context import PygameContext
from base.player import Player
from enemies.bullet_shooters import BulletShooters
from base.directions import get_direction
from base.bullets import Bullets


class Supermacy:
    def __init__(self):
        self.x = 100
        self.y = 300
        self.health = 4
        self.form = None
        self.team_x = 0
        self.team_y = 0
        self.enemy_x = 0
        self.enemy_y = 0
        self.dest_x = 0
        self.dest_y = 0
        self.dir_x = 0
        self.dir_y = 0
        self.speed = 2.5

    def draw(self, context: PygameContext):
        self.form = pygame.draw.rect(context.screen, (255, 0, 0), (self.x, self.y, 50, 75))

    def control(self, player: Player, bullet_shooters: BulletShooters):
        for bullet_shooter in bullet_shooters._elements:
            self.team_x = bullet_shooter._x
            self.team_y = bullet_shooter._y
            break

        self.enemy_x = player.x
        self.enemy_y = player.y

        if self.enemy_x > self.team_x:
            self.dest_x = ((self.enemy_x - self.team_x) // 2) + self.team_x
        else:
            self.dest_x = ((self.team_x - self.enemy_x) // 2) + self.enemy_x
        if self.enemy_y > self.team_y:
            self.dest_y = ((self.enemy_y - self.team_y) // 2) + self.team_y
        else:
            self.dest_y = ((self.team_y - self.enemy_y) // 2) + self.enemy_y

        self.move()

    def move(self):
        self.dir_x, self.dir_y = get_direction(self.x, self.y, self.dest_x, self.dest_y)
        self.x = self.x + self.dir_x * self.speed
        self.y = self.y + self.dir_y * self.speed

    def contacts(self, bullets: Bullets):
        for bullet in bullets.elements:
            if self.form.colliderect(bullet.form) and bullet.attacker == "friend":
                bullet.sharp = False
                self.health = self.health - 1


class Supermacys:
    def __init__(self):
        self.elements = []

    def spawn(self):
        self.elements.append(Supermacy())

    def empty(self) -> bool:
        return len(self.elements) == 0

    def draw(self, context: PygameContext):
        for supermacy in self.elements:
            supermacy.draw(context)

    def control(self, player: Player, bullet_shooters: BulletShooters):
        for supermacy in self.elements:
            supermacy.control(player, bullet_shooters)

    def contacts(self, bullets: Bullets):
        for supermacy in self.elements:
            supermacy.contacts(bullets)

        tmp_list = []
        for x in self.elements:
            if not x.health <= 0:
                tmp_list.append(x)
        self.elements = tmp_list
