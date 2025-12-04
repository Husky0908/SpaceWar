from base.context import PygameContext
from enemies.bullet_shooters import BulletShooters
from enemies.runners import Runners
from enemies.rocket_launchers import RocketLaunchers
from enemies.first_boss import FirstBoss
from enemies.supermacy import Supermacys
from enemies.heavy_gunner import HeavyGunners
from base.asteroids import Asteroids
from base.player import Player
from enemies.big_runner import BigRunner


class GameLogic:
    def __init__(self, game_difficulty: int, level: int, asteroids_time: int):
        self.level = level
        self.wave_time = 0
        self.wave = 1
        self.difficulty = game_difficulty
        self.asteroids_time = asteroids_time
        self.asteroids_shoot_time = 0

    def wave_logic(self, context: PygameContext, bullet_shooters: BulletShooters, runners: Runners, rocket_launchers: RocketLaunchers, first_boss: FirstBoss, supermacys: Supermacys, heavy_gunners: HeavyGunners, asteroids: Asteroids, player: Player, big_runner: BigRunner):

        if self.level == 1:

            if self.wave_time == 0:
                for i in range(4 + self.difficulty):
                    bullet_shooters.spawn(context)
            if bullet_shooters.empty() and self.wave == 1:
                self.wave_time = 1200

            if self.wave_time == 1200:
                self.wave = self.wave + 1
                for i in range(4 + self.difficulty):
                    bullet_shooters.spawn(context)
                for i in range(2 + self.difficulty):
                    runners.spawn(context)
            if bullet_shooters.empty() and len(runners.elements) == 0 and self.wave == 2:
                self.wave_time = 3600

            if self.wave_time == 3600:
                self.wave = self.wave + 1
                for i in range(4 + self.difficulty):
                    bullet_shooters.spawn(context)
                    runners.spawn(context)
            if bullet_shooters.empty() and len(runners.elements) == 0 and self.wave == 3:
                self.wave_time = 6000

            if self.wave_time == 6000:
                self.wave = self.wave + 1
                for i in range(8 + self.difficulty):
                    runners.spawn(context)
            if len(runners.elements) == 0 and self.wave == 4:
                self.wave_time = 9000

            if self.wave_time == 9000:
                self.wave = self.wave + 1
                for i in range(4 + self.difficulty):
                    bullet_shooters.spawn(context)
                for i in range(2 + self.difficulty):
                    rocket_launchers.spawn(context)
            if bullet_shooters.empty() and len(rocket_launchers.elements) == 0 and self.wave == 5:
                self.wave_time = 11000

            if self.wave_time == 11000:
                self.wave = self.wave + 1
                for i in range(3 + self.difficulty):
                    bullet_shooters.spawn(context)
                    rocket_launchers.spawn(context)
                for i in range(2 + self.difficulty):
                    runners.spawn(context)
            if bullet_shooters.empty() and len(rocket_launchers.elements) == 0 and len(
                    runners.elements) == 0 and self.wave == 6:
                self.wave_time = 14000

            if self.wave_time == 14000:
                self.wave = self.wave + 1
                for i in range(3 + self.difficulty):
                    rocket_launchers.spawn(context)
                    runners.spawn(context)
                for i in range(4 + self.difficulty):
                    bullet_shooters.spawn(context)
            if bullet_shooters.empty() and len(rocket_launchers.elements) == 0 and len(
                    runners.elements) == 0 and self.wave == 7:
                self.wave = self.wave + 1

            if self.wave == 8:
                first_boss.spawn()
                self.wave = 9

            if self.wave == 9 and not first_boss.live:
                self.wave_time = 0
                self.wave = 100

            if self.wave == 100 and self.wave_time >= 600:
                return True

        if self.level == 2:

            if self.wave_time == 0:
                for i in range(2 + self.difficulty):
                    bullet_shooters.spawn(context)
                    runners.spawn(context)
                    rocket_launchers.spawn(context)
                self.wave = 1
            if bullet_shooters.empty() and len(rocket_launchers.elements) == 0 and len(runners.elements) == 0 and self.wave == 1:
                self.wave_time = 1500

            if self.wave_time == 1500:
                self.wave = 2
                for i in range(5 + self.difficulty):
                    bullet_shooters.spawn(context)
                for i in range(3 + self.difficulty):
                    supermacys.spawn()
            if bullet_shooters.empty() and len(supermacys.elements) == 0 and self.wave == 2:
                self.wave_time = 4000

            if self.wave_time == 4000:
                self.wave = 3
                for i in range(2 + self.difficulty):
                    bullet_shooters.spawn(context)
                    rocket_launchers.spawn(context)
                heavy_gunners.spawn()
            if bullet_shooters.empty() and len(rocket_launchers.elements) == 0 and len(heavy_gunners.elements) == 0 and self.wave == 3:
                self.wave_time = 5500

            if self.wave_time == 5500:
                self.wave = 4
                for i in range(3 + self.difficulty):
                    heavy_gunners.spawn()
                for i in range(2 + self.difficulty):
                    rocket_launchers.spawn(context)
            if len(rocket_launchers.elements) == 0 and len(heavy_gunners.elements) == 0 and self.wave == 4:
                self.wave_time = 7500

            if self.wave_time == 7500:
                self.wave = 5
                for i in range(2 + self.difficulty):
                    heavy_gunners.spawn()
                for i in range(3 + self.difficulty):
                    bullet_shooters.spawn(context)
                    supermacys.spawn()
            if len(supermacys.elements) == 0 and len(heavy_gunners.elements) == 0 and bullet_shooters.empty() and self.wave == 5:
                self.wave_time = 9500

            if self.wave_time == 9500:
                big_runner.spawn()
                self.wave = 6

            if self.wave == 6 and not big_runner.live and len(runners.elements) == 0:
                self.wave = 100
                self.wave_time = 0

            if self.wave == 100 and self.wave_time >= 600:
                return True

        self.asteroids_shoot_time = self.asteroids_shoot_time + 1
        if self.asteroids_shoot_time == self.asteroids_time:
            asteroids.spawn(player)
            self.asteroids_shoot_time = 0

        self.wave_time = self.wave_time + 1

        return False
