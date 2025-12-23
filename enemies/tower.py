import pygame
import random
from base.context import PygameContext
from base.bullets import Bullets, Bullet
from base.player import Player
from base.bombs import Bomb, Bombs


class Tower:
    STATE_SHOOT = 1

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.form = None
        self.state = Tower.STATE_SHOOT
        self.shoot_time = 0
        self.shoot_time_end = random.randint(50, 70)
        self.health = 10

    def draw(self, context: PygameContext):
        self.form = pygame.draw.rect(context.screen, (0, 0, 255), (self.x, self.y, 70, 70))

    def control(self, bullets: Bullets, player: Player):
        if self.state == Tower.STATE_SHOOT:
            self.shoot_time = self.shoot_time + 1
            if self.shoot_time == self.shoot_time_end:
                en_x = player.x + random.randint(-100, 100)
                en_y = player.y + random.randint(-100, 100)
                bullets.elements.append(Bullet(self.x, self.y, en_x, en_y, "enemy", 400))
                self.shoot_time = 0


class Towers:
    def __init__(self):
        self.elements = []

    def spawn(self, context: PygameContext):
        spawn = True
        while spawn:
            x = random.randint(0, context.width - 70)
            y = random.randint(0, context.height - 70)
            spawn_x = True
            spawn_y = True
            spawn = False
            for tower in self.elements:
                if -100 < tower.x - x < 100:
                    spawn_x = False
                if -100 < tower.y - y < 100:
                    spawn_y = False
                if not spawn_x and not spawn_y:
                    spawn = True
                else:
                    spawn_x = True
                    spawn_y = True
        self.elements.append(Tower(x, y))

    def draw(self, context: PygameContext):
        for tower in self.elements:
            tower.draw(context)

    def control(self, bullets: Bullets, player: Player):
        for tower in self.elements:
            tower.control(bullets, player)

    def contacts(self, bullets: Bullets, bombs: Bombs):
        for tower in self.elements:
            for bullet in bullets.elements:
                if tower.form.colliderect(bullet.form) and bullet.attacker == "friend":
                    tower.health = tower.health - 1
                    bullet.sharp = False

            for bomb in bombs.elements:
                if tower.form.colliderect(bomb.form) and bomb.state == Bomb.STATE_EXPLOSION:
                    bomb.sharp = False
                    tower.health = tower.health - 5
                if tower.form.colliderect(bomb.form) and bomb.state == Bomb.STATE_MOVE:
                    bomb.state = Bomb.STATE_EXPLOSION

        tmp_list = []
        for x in self.elements:
            if not x.health <= 0:
                tmp_list.append(x)
        self.elements = tmp_list
