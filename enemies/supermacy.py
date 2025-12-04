import pygame
import random
from base.context import PygameContext
from base.player import Player
from enemies.bullet_shooters import BulletShooters
from base.directions import get_direction
from base.bullets import Bullet, Bullets
from base.boxes import PlusHealths, PlusHealth


class Supermacy:
    STATE_DEFEND = 1
    STATE_SURVIVE = 2
    STATE_KILLED = 3
    SURVIVE_LEFT = 1
    SURVIVE_RIGHT = 2

    def __init__(self, x: int):
        self.x = x
        self.y = random.randint(100, 500)
        self.health = 4
        self.form = None
        self.state = Supermacy.STATE_DEFEND
        self.state_survive = None
        self.move_px = 0
        self.team_x = 0
        self.team_y = 0
        self.enemy_x = 0
        self.enemy_y = 0
        self.dest_x = 0
        self.dest_y = 0
        self.dir_x = 0
        self.dir_y = 0
        self.speed = 2.5
        self.shoot_time = 0
        self.shoot_time_end = random.randint(240, 360)
        self.asteroid = False

    def draw(self, context: PygameContext):
        self.form = pygame.draw.rect(context.screen, (255, 0, 0), (self.x, self.y, 50, 75))

    def control(self, player: Player, bullet_shooters: BulletShooters, bullets: Bullets, b_n: int, plus_hp: PlusHealths):
        if not b_n == -1:
            self.state = Supermacy.STATE_DEFEND
            self.state_survive = None
            for bullet_shooter in bullet_shooters._elements:
                self.team_x = bullet_shooter._x
                self.team_y = bullet_shooter._y
                b_n = b_n - 1
                if b_n <= 0:
                    break
        else:
            self.state = Supermacy.STATE_SURVIVE

        self.enemy_x = player.x
        self.enemy_y = player.y

        if self.state == Supermacy.STATE_DEFEND:
            if self.enemy_x > self.team_x:
                self.dest_x = ((self.enemy_x - self.team_x) // 2) + self.team_x
            else:
                self.dest_x = ((self.team_x - self.enemy_x) // 2) + self.enemy_x
            if self.enemy_y > self.team_y:
                self.dest_y = ((self.enemy_y - self.team_y) // 2) + self.team_y
            else:
                self.dest_y = ((self.team_y - self.enemy_y) // 2) + self.enemy_y

            self.move()

        if self.state == Supermacy.STATE_SURVIVE:
            if self.y > 0:
                self.y = self.y - 2
            if self.state_survive is None:
                self.state_survive = random.randint(1, 2)
                self.move_px = random.randint(100, 300)
            if self.x <= 0:
                self.state_survive = 2
            if self.x >= 1230:
                self.state_survive = 1
            if self.state_survive == 1:
                self.x = self.x - 2
            else:
                self.x = self.x + 2
            self.move_px = self.move_px - 2
            if self.move_px <= 0:
                self.state_survive = None

        self.shoot(bullets, player)

        if self.health <= 0:
            chance = random.randint(1, 2)
            if chance == 2:
                plus_hp.elements.append(PlusHealth(self.x, self.y, 1))
            self.state = Supermacy.STATE_KILLED

    def move(self):
        self.dir_x, self.dir_y = get_direction(self.x, self.y, self.dest_x, self.dest_y)
        self.x = self.x + self.dir_x * self.speed
        self.y = self.y + self.dir_y * self.speed

    def contacts(self, bullets: Bullets):
        for bullet in bullets.elements:
            if self.form.colliderect(bullet.form) and bullet.attacker == "friend":
                bullet.sharp = False
                self.health = self.health - 1

    def shoot(self, bullets: Bullets, player: Player):
        if self.shoot_time - self.shoot_time_end >= 0:
            bullets.elements.append(Bullet(self.x, self.y, player.x, player.y, "enemy"))
            self.shoot_time = 0
            self.shoot_time_end = random.randint(240, 360)
        self.shoot_time = self.shoot_time + 1


class Supermacys:
    def __init__(self):
        self.elements = []

    def spawn(self):
        m_o_p = random.randint(1, 2)
        if m_o_p == 1:
            x = -75
        else:
            x = 1355
        self.elements.append(Supermacy(x))

    def empty(self) -> bool:
        return len(self.elements) == 0

    def draw(self, context: PygameContext):
        for supermacy in self.elements:
            supermacy.draw(context)

    def control(self, player: Player, bullet_shooters: BulletShooters, bullets: Bullets, plus_hp: PlusHealths):
        b_n = len(bullet_shooters._elements)
        if b_n == 0:
            b_n = -1
        for supermacy in self.elements:
            supermacy.control(player, bullet_shooters, bullets, b_n, plus_hp)
            b_n = b_n - 1
            if b_n <= 0:
                b_n = -1

    def contacts(self, bullets: Bullets):
        for supermacy in self.elements:
            supermacy.contacts(bullets)

        tmp_list = []
        for x in self.elements:
            if not x.state == Supermacy.STATE_KILLED:
                tmp_list.append(x)
        self.elements = tmp_list
