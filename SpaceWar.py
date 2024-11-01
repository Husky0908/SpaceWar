import pygame


class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.health = 5
        self.width = 20
        self.height = 40


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


class PygameContext:
    def __init__(self, width: int, height: int):
        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.delta_time = 0


def control_player(context: PygameContext, player: Player):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.y -= 300 * context.delta_time
    if keys[pygame.K_s]:
        player.y += 300 * context.delta_time
    if keys[pygame.K_a]:
        player.x -= 300 * context.delta_time
    if keys[pygame.K_d]:
        player.x += 300 * context.delta_time

    if player.y - player.height / 2 < 0:
        player.y = player.height / 2
    if player.y + player.height / 2 > context.height:
        player.y = context.height - player.height / 2
    if player.x - player.width / 2 < 0:
        player.x = player.width / 2
    if player.x + player.width / 2 > context.width:
        player.x = context.width - player.width / 2


def draw_player(context: PygameContext, player: Player):
    r = pygame.Rect(player.x - player.width / 2, player.y - player.height / 2, player.width, player.height)
    pygame.draw.rect(context.screen, (255, 255, 255), r)


def draw(context: PygameContext, player: Player):
    context.screen.fill((0, 0, 0))

    draw_player(context, player)

    pygame.display.flip()


def main():
    context = PygameContext(1280, 720)
    player = Player(context.width // 2, context.height // 2)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        control_player(context, player)
        draw(context, player)

        context.delta_time = context.clock.tick(60) / 1000

    pygame.quit()


main()
