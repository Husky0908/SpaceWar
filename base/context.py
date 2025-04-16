import pygame


class PygameContext:
    def __init__(self, width: int, height: int):
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("Space War")
        pygame.display.set_icon(pygame.image.load("Pictures/players_pictures/player_ship_4_hp_j.png"))

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.time = 0
