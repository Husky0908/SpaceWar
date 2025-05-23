import pygame
from base.context import PygameContext
from base.bullets import Bullets, Bullet
from texts.options_save import OptionsSave
from base.boxes import Coins, PlusHealths, Upgraders
from texts.text_print import print_text


class Player:
    def __init__(self, x: int, y: int):
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
        self.coins = 0
        self.coin_pictures = pygame.image.load("Pictures/other_pictures/coin_big.png")
        self.upgrader_pictures = pygame.image.load("Pictures/other_pictures/upgrader_box_big.png")
        self.upgrades_box = 0

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

    def control(self, context: PygameContext, running, options_save: OptionsSave):
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

        if self.health <= 0:
            running = True

        return running

    def press_mouse(self, running, bullets: Bullets, context: PygameContext):
        if running:
            if bullets.last_spawn - context.time >= 30:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                bullets.elements.append(Bullet(self.x, self.y, mouse_x, mouse_y, "friend"))
                bullets.last_spawn = context.time

    def get_rectangle_around_player(self, width: int, height: int) -> pygame.Rect:
        return pygame.Rect(self.x - width // 2, self.y - height // 2, width, height)
