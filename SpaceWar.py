import pygame
import random


class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.health = 5
        self.width = 20
        self.height = 40
        self.form = None


class Bullet_shooter:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.health = 2
        self.form = None
        self.STATE = Bullet_shooter.STATE_INIT

    height = 45
    width = 30
    STATE_INIT = 0
    STATE_FIRST_MOVE = 1
    STATE_FIRST_WAIT = 2
    STATE_SECOND_MOVE = 3
    STATE_SECOND_WAIT = 4
    STATE_THIRD_MOVE = 5
    STATE_THIRD_WAIT = 6
    STATE_KILLED = 7


class Runner:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.health = 5
        self.state = Runner.STATE_INIT
        self.x_0 = 0
        self.y_0 = 0
        self.dir_x = 0
        self.dir_y = 0
        self.start_time = 0
        self.form = None
        self.wounded = False

    height = 60
    width = 100
    STATE_INIT = 0
    STATE_SLOW_MOVE = 1
    STATE_FIRST_STOP = 2
    STATE_FAST_MOVE = 3
    STATE_SECOND_STOP = 4
    STATE_KILLED = 5

    SLOW_SPEED = 80
    FAST_SPEED = 650


class Runners:
    def __init__(self):
        self.last_spawn = 0
        self.elements = []


class Bullet:
    def __init__(self, x_0: int, y_0: int, destination_x: float, destination_y: float):
        self.x_0 = x_0
        self.y_0 = y_0
        self.x = x_0
        self.y = y_0
        self.dest_x = destination_x
        self.dest_y = destination_y
        self.dir_x = None
        self.dir_y = None
        self.speed = 400
        self.start_time = 0
        self.sharp = False
        self.form = None
        self.r = 10


class Bullets:
    def __init__(self):
        self.last_spawn = 100
        self.elements = []


class PygameContext:
    def __init__(self, width: int, height: int):
        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.time = 0


def length(x: int, x_2: int, y: int, y_2: int) -> float:
    e_x = x_2 - x
    e_y = y_2 - y
    leng = (e_x ** 2 + e_y ** 2) ** 0.5
    return leng


def get_direction(x_1: int, y_1: int, x_2: int, y_2: int) -> tuple[float, float]:
    leng = length(x_1, x_2, y_1, y_2)
    return (x_2 - x_1) / leng, (y_2 - y_1) / leng


def shoot_bullet(bullets: Bullets, player: Player, context: PygameContext):
    if bullets.last_spawn - context.time >= 30:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        bullets.elements.append(Bullet(player.x, player.y, mouse_x, mouse_y))
        bullets.last_spawn = context.time


def control_bullets(bullets: Bullets, context: PygameContext, runners: Runners):
    bullets.last_spawn = bullets.last_spawn + 1
    for bullet in bullets.elements:
        if bullet.sharp:
            d_t = context.time - bullet.start_time
            bullet.x = bullet.x_0 + bullet.dir_x * d_t * bullet.speed
            bullet.y = bullet.y_0 + bullet.dir_y * d_t * bullet.speed
            if bullet.x >= context.width or bullet.x <= 0 or bullet.y >= context.height or bullet.y <= 0:
                del bullet
        else:
            bullet.dir_x, bullet.dir_y = get_direction(bullet.x, bullet.y, bullet.dest_x, bullet.dest_y)
            bullet.start_time = context.time
            bullet.sharp = True


def press_mouse(running, bullets: Bullets, player: Player, context: PygameContext):
    if running:
        shoot_bullet(bullets, player, context)


def get_rectangle_around_player(player: Player, width: int, height: int) -> pygame.Rect:
    return pygame.Rect(player.x - width // 2, player.y - height // 2, width, height)


def control_player(context: PygameContext, player: Player, running):
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

    if player.health <= 0:
        running = False

    return running


def spawn_runners(context: PygameContext, player: Player, runners: Runners):
    if context.time - runners.last_spawn >= 5:
        runners.last_spawn = context.time
        trying = True
        while trying:
            x = random.randint((0 + Runner.width // 2), context.width - Runner.width // 2)
            y = random.randint(0 + Runner.height // 2, context.height - Runner.height // 2)
            leng = length(player.x, x, player.y, y)
            if leng >= 600:
                trying = False
                runners.elements.append(Runner(x, y))


def destination_runner(player: Player, widht, height):
    rect = get_rectangle_around_player(player, widht, height)
    dest_x = random.randint(rect.left, rect.right)
    dest_y = random.randint(rect.top, rect.bottom)
    return dest_x, dest_y


def control_runners(context: PygameContext, player: Player, runners: Runners, bullets: Bullets):
    for runner in runners.elements:
        if runner.state == Runner.STATE_INIT:
            runner.state = Runner.STATE_SLOW_MOVE
            dest_x, dest_y = destination_runner(player, 100, 100)
            runner.dir_x, runner.dir_y = get_direction(runner.x, runner.y, dest_x, dest_y)
            runner.start_time = context.time
            runner.x_0, runner.y_0 = runner.x, runner.y
        elif runner.state == Runner.STATE_SLOW_MOVE:
            d_t = context.time - runner.start_time
            if d_t < 5:
                runner.x = runner.x_0 + runner.dir_x * d_t * Runner.SLOW_SPEED
                runner.y = runner.y_0 + runner.dir_y * d_t * Runner.SLOW_SPEED
            else:
                runner.state = Runner.STATE_FIRST_STOP
                runner.start_time = context.time
        if runner.state == Runner.STATE_FIRST_STOP:
            if context.time - runner.start_time >= 3:
                runner.state = Runner.STATE_FAST_MOVE
                runner.wounded = False
                dest_x, dest_y = destination_runner(player, 0, 0)
                runner.dir_x, runner.dir_y = get_direction(runner.x, runner.y, dest_x, dest_y)
                runner.start_time = context.time
                runner.x_0, runner.y_0 = runner.x, runner.y
        if runner.state == Runner.STATE_FAST_MOVE:
            d_t = context.time - runner.start_time
            runner.x = runner.x_0 + runner.dir_x * d_t * Runner.FAST_SPEED
            runner.y = runner.y_0 + runner.dir_y * d_t * Runner.FAST_SPEED
            if runner.form.colliderect(player.form) and not runner.wounded:
                player.health = player.health - 1
                runner.wounded = True
            if runner.x > context.width - runner.width / 2 or runner.x < runner.width / 2 or runner.y > context.height - runner.height / 2 or runner.y < runner.height / 2:
                runner.state = Runner.STATE_SECOND_STOP
                runner.start_time = context.time
        if runner.state == Runner.STATE_SECOND_STOP:
            if context.time - runner.start_time >= 3:
                runner.state = Runner.STATE_INIT
        if runner.health <= 0:
            runner.state = Runner.STATE_KILLED
        if runner.state == Runner.STATE_KILLED:
            del runner
        # for bullet in bullets.elements:
        #     if runner.form.colliderect(bullet.form):
        #         runner.health = runner.health - 1


def control(context: PygameContext, player: Player, runners: Runners, bullets: Bullets):
    spawn_runners(context, player, runners)
    control_runners(context, player, runners, bullets)
    control_bullets(bullets, context, runners)


def draw_player(context: PygameContext, player: Player):
    r = pygame.Rect(player.x - player.width / 2, player.y - player.height / 2, player.width, player.height)
    player.form = pygame.draw.rect(context.screen, (255, 255, 255), r)


def draw_bullets(context: PygameContext, bullets: Bullets):
    for bullet in bullets.elements:
        bullet.form = pygame.draw.circle(context.screen, (255, 0, 0), (bullet.x, bullet.y), bullet.r)


def draw_mouse(context: PygameContext):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pygame.draw.circle(context.screen, (255, 255, 255), (mouse_x, mouse_y), 10)


def draw_runners(context: PygameContext, runners: Runners):
    for runner in runners.elements:
        r = pygame.Rect(runner.x - runner.width / 2, runner.y - runner.height / 2, runner.width, runner.height)
        runner.form = pygame.draw.rect(context.screen, (0, 255, 0), r)


def draw(context: PygameContext, player: Player, runners: Runners, bullets: Bullets):
    context.screen.fill((0, 0, 0))

    draw_player(context, player)
    draw_mouse(context)
    draw_bullets(context, bullets)
    draw_runners(context, runners)

    pygame.display.flip()


def main():
    context = PygameContext(1280, 720)
    player = Player(context.width // 2, context.height // 2)

    bullets = Bullets()
    runners = Runners()

    pygame.mouse.set_visible(False)
    pygame.display.set_caption("Space War")

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                press_mouse(running, bullets, player, context)

        running = control_player(context, player, running)
        control(context, player, runners, bullets)
        draw(context, player, runners, bullets)

        context.delta_time = context.clock.tick(60) / 1000
        context.time = context.time + context.delta_time

    pygame.quit()


main()
