import pygame
import random
from base.context import PygameContext
from base.bullets import Bullets, Bullet
from texts.options_save import OptionsSave
from base.boxes import Coins, PlusHealths, Upgraders
from texts.text_print import print_text
from base.bombs import Bombs, Bomb


class Player:
    def __init__(self, x: int, y: int, name: str):
        self.x = x
        self.y = y
        self.health = 5
        self.width = 20
        self.height = 40
        self.form = None
        self.crosshair_form = pygame.image.load("Pictures/players_pictures/crosshair.png").convert_alpha()
        self.pictures = [pygame.image.load("Pictures/players_pictures/player_ship_1_hp_j.png").convert_alpha(), pygame.image.load(
            "Pictures/players_pictures/player_ship_2_hp_j.png").convert_alpha(), pygame.image.load(
            "Pictures/players_pictures/player_ship_3_hp_j.png").convert_alpha(), pygame.image.load(
            "Pictures/players_pictures/player_ship_4_hp_j.png").convert_alpha(), pygame.image.load(
            "Pictures/players_pictures/player_ship_5_hp_j.png").convert_alpha()]
        self.r = None
        self.name = name
        self.coins = 0
        self.coin_pictures = pygame.image.load("Pictures/other_pictures/coin_big.png")
        self.upgrader_pictures = pygame.image.load("Pictures/other_pictures/upgrader_box_big.png")
        self.upgrades_box = 0
        self.dif = 0
        self.level = 1
        self.unlock_levels = 1
        self.ship_power = 1
        self.gun_power = 1
        self.bomb_power = 0
        self.rocket_power = 0
        self.skins = 0
        self.read_player_text()

    def read_player_text(self):
        with open(f"texts/players/{self.name}", "r") as f:
            self.dif = int(f.readline().strip("\n"))
            self.level = int(f.readline().strip("\n"))
            self.unlock_levels = int(f.readline().strip("\n"))
            self.coins = int(f.readline().strip("\n"))
            self.upgrades_box = int(f.readline().strip("\n"))
            self.ship_power = int(f.readline().strip("\n"))
            self.gun_power = int(f.readline().strip("\n"))
            self.bomb_power = int(f.readline().strip("\n"))
            self.rocket_power = int(f.readline().strip("\n"))
            self.skins = int(f.readline().strip("\n"))

    def write_player_text(self):
        with open(f"texts/players/{self.name}", "w") as f:
            f.write(f"{self.dif}\n")
            f.write(f"{self.level}\n")
            f.write(f"{self.unlock_levels}\n")
            f.write(f"{self.coins}\n")
            f.write(f"{self.upgrades_box}\n")
            f.write(f"{self.ship_power}\n")
            f.write(f"{self.gun_power}\n")
            f.write(f"{self.bomb_power}\n")
            f.write(f"{self.rocket_power}\n")
            f.write(f"{self.skins}\n")

    def picture(self, context: PygameContext):
        if self.health < 6:
            self.form = context.screen.blit(self.pictures[self.health - 1], self.r)
        else:
            self.form = context.screen.blit(self.pictures[4], self.r)

    def draw(self, context: PygameContext):
        self.r = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)

        if self.health < 6:
            hmp = 15
            color = (255, 0, 0)
            if self.health == 2:
                color = (255, 128, 0)
            if self.health == 3:
                color = (255, 255, 0)
            if self.health == 4:
                color = (128, 255, 0)
            if self.health == 5:
                color = (0, 255, 0)
            for i in range(self.health):
                pygame.draw.rect(context.screen, color, (hmp, context.height - 50, 15, 40))
                hmp = hmp + 20

        context.screen.blit(self.coin_pictures, (context.width - 200, context.height - 75))
        print_text(str(self.coins), 60, (255, 255, 255), (context.width - 75, context.height - 35), context)
        context.screen.blit(self.upgrader_pictures, (context.width - 400, context.height - 70))
        print_text(str(self.upgrades_box), 60, (255, 255, 255), (context.width - 250, context.height - 35), context)

        if self.health > 0:
            self.picture(context)

    def contacts(self, bullets: Bullets, coins: Coins, plus_hp: PlusHealths, upgrades: Upgraders):
        for bullet in bullets.elements:
            if bullet.form.colliderect(self.form) and bullet.attacker == "enemy":
                if self.ship_power == 2:
                    shield = random.randint(0, 100)
                    if shield <= 5:
                        self.health = self.health + 1
                self.health = self.health - 1
                bullet.sharp = False

        for coin in coins.elements:
            if coin.form.colliderect(self.form):
                self.coins = self.coins + coin.value
                coin.delete = True

        for plus_h in plus_hp.elements:
            if plus_h.form.colliderect(self.form) and self.health < 5:
                self.health = self.health + plus_h.value
                if self.health > 5:
                    self.health = 5
                plus_h.delete = True

        for upgrade in upgrades.elements:
            if upgrade.form.colliderect(self.form):
                self.upgrades_box = self.upgrades_box + upgrade.value
                upgrade.delete = True

    def control(self, context: PygameContext, running, options_save: OptionsSave, bullets: Bullets, bombs: Bombs):
        keys = pygame.key.get_pressed()
        if keys[options_save.up_control]:
            self.y -= 300 * context.delta_time
        if keys[options_save.down_control]:
            self.y += 300 * context.delta_time
        if keys[options_save.left_control]:
            self.x -= 300 * context.delta_time
        if keys[options_save.right_control]:
            self.x += 300 * context.delta_time

        if self.y - self.height / 2 < 0:
            self.y = self.height / 2
        if self.y + self.height / 2 > context.height:
            self.y = context.height - self.height / 2
        if self.x - self.width / 2 < 0:
            self.x = self.width / 2
        if self.x + self.width / 2 > context.width:
            self.x = context.width - self.width / 2

        mouse_button = pygame.mouse.get_pressed()
        if mouse_button[0]:
            self.mashingun_shoot(True, bullets, context)
        if mouse_button[2]:
            if self.bomb_power >= 1:
                self.bomb_shoot(True, context, bombs)

        if self.health <= 0:
            self.write_player_text()
            running = True

        return running

    def mashingun_shoot(self, running, bullets: Bullets, context: PygameContext):
        if running:
            shoot_time = 30
            if self.gun_power == 2:
                shoot_time = 25
            if self.gun_power == 3:
                shoot_time = 20
            if self.gun_power == 4:
                shoot_time = 15
            if bullets.last_spawn - context.time >= shoot_time:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                bullets.elements.append(Bullet(self.x, self.y, mouse_x, mouse_y, "friend"))
                bullets.last_spawn = context.time

    def bomb_shoot(self, running, context: PygameContext, bombs: Bombs):
        if running:
            shoot_time = 60
            if bombs.last_spawn - context.time >= shoot_time:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                bombs.elements.append(Bomb(self.x, self.y, mouse_x, mouse_y, "friend"))
                bombs.last_spawn = context.time

    def get_rectangle_around_player(self, width: int, height: int) -> pygame.Rect:
        return pygame.Rect(self.x - width // 2, self.y - height // 2, width, height)
