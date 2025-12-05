import pygame
import random
from base.context import PygameContext
from base.player import Player
from enemies.bullet_shooters import BulletShooters
from enemies.runners import Runners
from enemies.rocket_launchers import RocketLaunchers
from enemies.supermacy import Supermacys
from enemies.heavy_gunner import HeavyGunners
from base.bullets import Bullets
from base.rockets import Rockets, Rocket
from base.bombs import Bomb, Bombs


class Asteroid:
    STATE_INIT = 0
    STATE_MOVE = 1
    STATE_DESTROY = 2

    def __init__(self, x: int, y: int, dir: int):
        self.x = x
        self.y = y
        self.damage = False
        self.form = None
        self.direction = dir
        self.state = Asteroid.STATE_INIT
        self.init_time = 0

    def draw(self, context: PygameContext):
        self.form = pygame.draw.rect(context.screen, (255, 255, 255), (self.x, self.y, 150, 150))
        if self.state == Asteroid.STATE_INIT:
            if self.direction == -1:
                x = 1205
            else:
                x = 75
            pygame.draw.rect(context.screen, (255, 255, 0), (x, self.y + 50, 50, 50))

    def control(self, context: PygameContext, player: Player, bullet_shooters: BulletShooters, runners: Runners, rocket_launchers: RocketLaunchers, supermacys: Supermacys, heavy_gunners: HeavyGunners):
        if self.state == Asteroid.STATE_INIT:
            self.init_time = self.init_time + 1
            if self.init_time >= 120:
                self.state = Asteroid.STATE_MOVE
        if self.state == Asteroid.STATE_MOVE:
            self.x = self.x + 400 * context.delta_time * self.direction
            # self.x = self.x + 7 * self.direction
            if self.direction == -1 and self.x <= -150:
                self.state = Asteroid.STATE_DESTROY
            if self.direction == 1 and self.x >= 1280:
                self.state = Asteroid.STATE_DESTROY
        if self.state == Asteroid.STATE_DESTROY:
            for bullet_shooter in bullet_shooters._elements:
                bullet_shooter.asteroid = False

            for heavy_gunner in heavy_gunners.elements:
                heavy_gunner.asteroid = False

            for runner in runners.elements:
                runner.asteroid = False

            for supermacy in supermacys.elements:
                supermacy.asteroid = False

            for rocket_launcher in rocket_launchers.elements:
                rocket_launcher.asteroid = False

    def contacts(self, context: PygameContext, player: Player, bullet_shooters: BulletShooters, runners: Runners, rocket_launchers: RocketLaunchers, supermacys: Supermacys, heavy_gunners: HeavyGunners, bullets: Bullets, rockets: Rockets, bombs: Bombs):

        if self.form.colliderect(player.form) and not self.damage:
            if player.ship_power == 2:
                shield = random.randint(0, 100)
                if shield <= 5:
                    player.health = player.health + 1
            player.health = player.health - 1
            self.damage = True

        for bullet_shooter in bullet_shooters._elements:
            if self.form.colliderect(bullet_shooter._form) and not bullet_shooter.asteroid:
                bullet_shooter._health = bullet_shooter._health - 1
                bullet_shooter.asteroid = True

        for heavy_gunner in heavy_gunners.elements:
            if self.form.colliderect(heavy_gunner.form) and not heavy_gunner.asteroid:
                heavy_gunner.health = heavy_gunner.health - 1
                heavy_gunner.asteroid = True

        for runner in runners.elements:
            if self.form.colliderect(runner.r) and not runner.asteroid:
                runner.health = runner.health - 1
                runner.asteroid = True

        for supermacy in supermacys.elements:
            if self.form.colliderect(supermacy.form) and not supermacy.asteroid:
                supermacy.health = supermacy.health - 1
                supermacy.asteroid = True

        for rocket_launcher in rocket_launchers.elements:
            if self.form.colliderect(rocket_launcher.form) and not rocket_launcher.asteroid:
                rocket_launcher.health = rocket_launcher.health - 1
                rocket_launcher.asteroid = True

        for bullet in bullets.elements:
            if self.form.colliderect(bullet.form):
                bullet.sharp = False

        for rocket in rockets.elements:
            if self.form.colliderect(rocket.form):
                rocket.state = Rocket.STATE_DESTROY

        for bomb in bombs.elements:
            if self.form.colliderect(bomb.form) and bomb.state == Bomb.STATE_EXPLOSION:
                bomb.sharp = False
            if self.form.colliderect(bomb.form) and bomb.state == Bomb.STATE_MOVE:
                bomb.state = Bomb.STATE_EXPLOSION


class Asteroids():
    def __init__(self):
        self.elements = []

    def draw(self, context: PygameContext):
        for asteroid in self.elements:
            asteroid.draw(context)

    def spawn(self, player: Player):
        dir = random.randint(1, 2)
        if dir == 2:
            x = 1480
            dir = -1
        else:
            x = -200
        y = player.y - 50
        self.elements.append(Asteroid(x, y, dir))

    def control(self, context: PygameContext, player: Player, bullet_shooters: BulletShooters, runners: Runners, rocket_launchers: RocketLaunchers, supermacys: Supermacys, heavy_gunners: HeavyGunners):
        for asteroid in self.elements:
            asteroid.control(context, player, bullet_shooters, runners, rocket_launchers, supermacys, heavy_gunners)

    def contacts(self, context: PygameContext, player: Player, bullet_shooters: BulletShooters, runners: Runners, rocket_launchers: RocketLaunchers, supermacys: Supermacys, heavy_gunner: HeavyGunners, bullets: Bullets, rockets: Rockets, bombs: Bombs):
        for asteroid in self.elements:
            asteroid.contacts(context, player, bullet_shooters, runners, rocket_launchers, supermacys, heavy_gunner, bullets, rockets, bombs)

        tmp_list = []
        for x in self.elements:
            if not x.state == Asteroid.STATE_DESTROY:
                tmp_list.append(x)
        self.elements = tmp_list
