import pygame
from base.context import PygameContext
from base.bullets import Bullets, Bullet


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

    def picture(self, context: PygameContext):
        if self.health < 6:
            self.form = self.pictures[self.health - 1]
        else:
            self.form = self.pictures[4]

    def draw(self, context: PygameContext):
        self.r = pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
        self.picture(context)
        context.screen.blit(self.form, self.r)

    def contacts(self, bullets: Bullets):
        for bullet in bullets.elements:
            if bullet.form.colliderect(self.r) and bullet.attacker == "enemy":
                self.health = self.health - 1
                bullet.sharp = False


    def control(self, context: PygameContext, running):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.y -= 300 * context.delta_time
        if keys[pygame.K_s]:
            self.y += 300 * context.delta_time
        if keys[pygame.K_a]:
            self.x -= 300 * context.delta_time
        if keys[pygame.K_d]:
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
            running = False

        return running

    def press_mouse(self, running, bullets: Bullets, context: PygameContext):
        if running:
            if bullets.last_spawn - context.time >= 30:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                bullets.elements.append(Bullet(self.x, self.y, mouse_x, mouse_y, "friend"))
                bullets.last_spawn = context.time

    def get_rectangle_around_player(self, width: int, height: int) -> pygame.Rect:
        return pygame.Rect(self.x - width // 2, self.y - height // 2, width, height)
