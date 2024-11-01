import pygame


class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.health = 5


class Runner:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.health = 5


class Bullet:
    def __init__(self, x_0: int, y_0: int, direction_x: float, direction_y: float):
        self.x_0 = x_0
        self.y_0 = y_0
        self.x = x_0
        self.y = y_0
        self.dir_x = direction_x
        self.dir_y = direction_y
        self.speed = 3


class PygameContex:
    def __init__(self, width: int, height: int):
        pygame.init()

        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()


def draw_player(contex: PygameContex, player: Player):
    r = pygame.Rect(player.x - 10, player.y - 20, 20, 40)
    pygame.draw.rect(contex.screen, (255, 255, 255), r)


def draw(contex: PygameContex, player: Player):
    contex.screen.fill((0, 0, 0))

    draw_player(contex, player)

    pygame.display.flip()


def main():
    width = 1280
    height = 720

    contex = PygameContex(width, height)
    player = Player(width // 2, height // 2)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw(contex, player)

        contex.clock.tick(60)  # limits FPS to 60


    pygame.quit()

main()
