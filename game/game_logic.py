from base.context import PygameContext
from enemies.bullet_shooters import BulletShooters
from enemies.runners import Runners
from enemies.rocket_launchers import RocketLaunchers
from enemies.first_boss import FirstBoss


class GameLogic:
    def __init__(self, game_difficulty: int):
        self.level = 1
        self.wave_time = 0
        self.wave = 1
        self.difficulty = game_difficulty

    def wave_logic(self, context: PygameContext, bullet_shooters: BulletShooters, runners: Runners, rocket_launchers: RocketLaunchers, first_boss: FirstBoss):
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

            self.wave_time = self.wave_time + 1
