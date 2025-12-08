import pygame
import random
from base.context import PygameContext
from base.bullets import Bullets, Bullet
from base.player import Player
from base.boxes import Coins, Coin
from base.bombs import Bombs, Bomb


class BulletShooter:
    height = 45
    width = 30
    STATE_INIT = 0
    STATE_MOVE_RIGHT = 1
    STATE_MOVE_LEFT = 2
    STATE_MOVE_DOWN = 3
    STATE_MOVE_UP = 4
    STATE_WAIT = 5
    STATE_NEXT = 6
    STATE_KILLED = 7

    next_id = 0

    def __init__(self, x: int, y: int):
        self._id = BulletShooter.next_id
        BulletShooter.next_id = BulletShooter.next_id + 1
        self._x = x
        self._y = y
        self._health = 2
        self._form = None
        self._forms = [pygame.image.load("Pictures/enemies_pictures/bullet_shooters/bullet_shooter_1_hp.png"), pygame.image.load("Pictures/enemies_pictures/bullet_shooters/bullet_shooter_2_hp.png")]
        self._r = None
        self._STATE = BulletShooter.STATE_INIT
        self._how_many_pixel = None
        self._wait_time = 0
        self._how_many_stop_time = 120
        self._how_many_pixel_min = 50
        self._how_many_pixel_max = 200
        self._shoot_time = 0
        self._shoot_time_end = 0
        self.asteroid = False

    def control(self, context: PygameContext, player: Player, bullets: Bullets, coins: Coins):
        if self._STATE == BulletShooter.STATE_INIT:
            self._handle_init()
        if self._STATE == BulletShooter.STATE_MOVE_RIGHT or self._STATE == BulletShooter.STATE_MOVE_LEFT or \
           self._STATE == BulletShooter.STATE_MOVE_DOWN or self._STATE == BulletShooter.STATE_MOVE_UP:
            self._handle_moves(context)
        if self._STATE == BulletShooter.STATE_WAIT:
            self._handle_wait()
        if self._STATE == BulletShooter.STATE_NEXT:
            self._handle_next_action()

        if self._STATE != BulletShooter.STATE_INIT:
            self._handle_shoot(player, bullets)

        if self._health <= 0:
            chance = random.randint(1, 10)
            if chance > 5:
                if chance > 7:
                    coins.elements.append(Coin(self._x, self._y, (1 * 10)))
                else:
                    coins.elements.append(Coin(self._x, self._y, (1 * 5)))
            self._STATE = BulletShooter.STATE_KILLED

    def contacts(self, context: PygameContext, bullets: Bullets, bombs: Bombs):
        for bullet in bullets.elements:
            if self._form.colliderect(bullet.form) and bullet.attacker == "friend":
                self._health = self._health - 1
                bullet.sharp = False

        for bomb in bombs.elements:
            if self._form.colliderect(bomb.form) and bomb.state == Bomb.STATE_EXPLOSION:
                bomb.sharp = False
                self._health = self._health - 2
            if self._form.colliderect(bomb.form) and bomb.state == Bomb.STATE_MOVE:
                bomb.state = Bomb.STATE_EXPLOSION

    def draw(self, context: PygameContext):
        self._r = pygame.Rect(self._x - BulletShooter.width / 2, self._y - BulletShooter.height / 2, BulletShooter.width, BulletShooter.height)
        if self._health == 2:
            self._form = context.screen.blit(self._forms[1], self._r)
        else:
            self._form = context.screen.blit(self._forms[0], self._r)

    def is_killed(self) -> bool:
        return self._STATE == BulletShooter.STATE_KILLED

    def _handle_init(self):
        self._y = self._y + 1
        if self._y >= 60:
            self._shoot_time_end = random.randint(80, 150)
            self._STATE = BulletShooter.STATE_NEXT

    def _handle_moves(self, context: PygameContext):
        if self._STATE == BulletShooter.STATE_MOVE_RIGHT:
            self._x = self._x + 1
            self._how_many_pixel = self._how_many_pixel - 1
            if self._how_many_pixel <= 0 or self._x >= context.width - BulletShooter.width / 2:
                self._STATE = BulletShooter.STATE_NEXT
        if self._STATE == BulletShooter.STATE_MOVE_LEFT:
            self._x = self._x - 1
            self._how_many_pixel = self._how_many_pixel - 1
            if self._how_many_pixel <= 0 or self._x <= BulletShooter.width / 2:
                self._STATE = BulletShooter.STATE_NEXT
        if self._STATE == BulletShooter.STATE_MOVE_DOWN:
            self._y = self._y + 1
            self._how_many_pixel = self._how_many_pixel - 1
            if self._how_many_pixel <= 0 or self._y >= context.height - BulletShooter.height / 2:
                self._STATE = BulletShooter.STATE_NEXT
        if self._STATE == BulletShooter.STATE_MOVE_UP:
            self._y = self._y - 1
            self._how_many_pixel = self._how_many_pixel - 1
            if self._how_many_pixel <= 0 or self._y <= BulletShooter.height / 2:
                self._STATE = BulletShooter.STATE_NEXT

    def _handle_wait(self):
        self._wait_time = self._wait_time - 1
        if self._wait_time == 0:
            self._STATE = BulletShooter.STATE_NEXT

    def _handle_next_action(self):
        next_state = random.randint(1, 5)
        self._how_many_pixel = random.randint(self._how_many_pixel_min, self._how_many_pixel_max)
        self._wait_time = random.randint(1 * 60, 3 * 60)
        self._STATE = next_state

    def _handle_shoot(self, player: Player, bullets: Bullets):
        self._shoot_time = self._shoot_time + 1
        if self._shoot_time == self._shoot_time_end:
            bullets.elements.append(Bullet(self._x, self._y, player.x, player.y, "enemy", 400))
            self._shoot_time = 0
            self._shoot_time_end = random.randint(80, 150)


class BulletShooters:
    def __init__(self):
        self._elements = []

    def spawn(self, context: PygameContext):
        x = random.randint((0 + BulletShooter.width // 2), context.width - BulletShooter.width // 2)
        y = 0 - BulletShooter.height
        self._elements.append(BulletShooter(x, y))

    def empty(self) -> bool:
        return len(self._elements) == 0

    def control(self, context: PygameContext, player: Player, bullets: Bullets, coins: Coins):
        for bullet_shooter in self._elements:
            bullet_shooter.control(context, player, bullets, coins)

    def contacts(self, context: PygameContext, bullets: Bullets, bombs: Bombs):
        for bullet_shooter in self._elements:
            bullet_shooter.contacts(context, bullets, bombs)

        tmp_list = []
        for x in self._elements:
            if not x.is_killed():
                tmp_list.append(x)
        self._elements = tmp_list

    def draw(self, context: PygameContext):
        for bullet_shooter in self._elements:
            bullet_shooter.draw(context)
