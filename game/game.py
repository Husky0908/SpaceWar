import pygame
import random

from base.context import PygameContext
from base.bullets import Bullets, Bullet
from base.player import Player
from enemies.bullet_shooters import BulletShooters

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
        self.r = None
        self.run_time = 0

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


class RocketLauncher:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.x_0 = x
        self.y_0 = y
        self.dest_x = None
        self.dest_y = None
        self.dir_x = None
        self.dir_y = None
        self.health = 4
        self.STATE = RocketLauncher.STATE_INIT
        self.form = None
        self.start_time = 0
        self.speed = 75

    height = 50
    width = 50
    STATE_INIT = 0
    STATE_MOVE = 1
    STATE_WAIT = 2
    STATE_SHOOT = 3
    STATE_KILL = 4


class RocketLaunchers:
    def __init__(self):
        self.last_spawn = 0
        self.elements = []


class Rocket:
    def __init__(self, x: int, y: int, attacker: str):
        self.x = x
        self.y = y
        self.health = 1
        self.dest_x = None
        self.dest_y = None
        self.dir_x = None
        self.dir_y = None
        self.speed = 3
        self.form = None
        self.r = 10
        self.attacker = attacker
        self.state = Rocket.STATE_MOVE
        self.time = 0

    height = 25
    width = 25

    STATE_MOVE = 1
    STATE_DESTROY = 2


class Rockets:
    def __init__(self):
        self.elements = []


class GameLogic:
    def __init__(self):
        self.level = 1
        self.wave_time = 0
        self.wave = 1


def length(x: int, x_2: int, y: int, y_2: int) -> float:
    e_x = x_2 - x
    e_y = y_2 - y
    leng = (e_x ** 2 + e_y ** 2) ** 0.5
    return leng


def get_direction(x_1: int, y_1: int, x_2: int, y_2: int) -> tuple[float, float]:
    leng = length(x_1, x_2, y_1, y_2)
    return (x_2 - x_1) / leng, (y_2 - y_1) / leng


def control_bullets(bullets: Bullets, context: PygameContext, runners: Runners):
    bullets.last_spawn = bullets.last_spawn + 1
    for bullet in bullets.elements:
        if bullet.sharp:
            d_t = context.time - bullet.start_time
            bullet.x = bullet.x_0 + bullet.dir_x * d_t * bullet.speed
            bullet.y = bullet.y_0 + bullet.dir_y * d_t * bullet.speed
            if bullet.x >= context.width or bullet.x <= 0 or bullet.y >= context.height or bullet.y <= 0:
                bullet.sharp = False
        else:
            bullet.dir_x, bullet.dir_y = get_direction(bullet.x, bullet.y, bullet.dest_x, bullet.dest_y)
            bullet.start_time = context.time
            bullet.sharp = True


def press_mouse(running, bullets: Bullets, player: Player, context: PygameContext, bullet_shooters: BulletShooters):
    if running:
        if bullets.last_spawn - context.time >= 30:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bullets.elements.append(Bullet(player.x, player.y, mouse_x, mouse_y, "friend"))
            bullets.last_spawn = context.time


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
        p_o_n = random.randint(1, 2)
        if p_o_n == 1:
            x = 0 - Runner.width
        else:
            x = context.width + Runner.width
        y = random.randint((0 - Runner.height), (context.height + Runner.height))
        runners.elements.append(Runner(x, y))


def spawn_rocket_launchers(context: PygameContext, player: Player, rocket_launchers: RocketLaunchers):
    x = random.randint(0, context.width)
    y = -RocketLauncher.height
    rocket_launchers.elements.append(RocketLauncher(x, y))


def spawn_rockets(rockets: Rockets, x, y, attacker):
    rockets.elements.append(Rocket(x, y, attacker))


def destination_runner(player: Player, width, height):
    rect = get_rectangle_around_player(player, width, height)
    dest_x = random.randint(rect.left, rect.right)
    dest_y = random.randint(rect.top, rect.bottom)
    return dest_x, dest_y


def control_runners(context: PygameContext, player: Player, runners: Runners, bullets: Bullets):
    for runner in runners.elements:
        if runner.state == Runner.STATE_INIT:
            runner.run_time = random.randint(3, 6)
            runner.state = Runner.STATE_SLOW_MOVE
            dest_x, dest_y = destination_runner(player, 100, 100)
            runner.dir_x, runner.dir_y = get_direction(runner.x, runner.y, dest_x, dest_y)
            runner.start_time = context.time
            runner.x_0, runner.y_0 = runner.x, runner.y
        elif runner.state == Runner.STATE_SLOW_MOVE:
            d_t = context.time - runner.start_time
            if d_t < runner.run_time:
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
                dest_x = dest_x
                dest_y =dest_y
                runner.dir_x, runner.dir_y = get_direction(runner.x, runner.y, dest_x, dest_y)
                runner.start_time = context.time
                runner.x_0, runner.y_0 = runner.x, runner.y
        if runner.state == Runner.STATE_FAST_MOVE:
            d_t = context.time - runner.start_time
            runner.x = runner.x_0 + runner.dir_x * d_t * Runner.FAST_SPEED
            runner.y = runner.y_0 + runner.dir_y * d_t * Runner.FAST_SPEED
            if runner.x > context.width - runner.width / 2 or runner.x < runner.width / 2 or runner.y > context.height - runner.height / 2 or runner.y < runner.height / 2:
                runner.state = Runner.STATE_SECOND_STOP
                runner.start_time = context.time
        if runner.state == Runner.STATE_SECOND_STOP:
            if context.time - runner.start_time >= 3:
                runner.state = Runner.STATE_INIT
        if runner.health <= 0:
            runner.state = Runner.STATE_KILLED


def control_rocket_launchers(context: PygameContext, player: Player, rocket_launchers: RocketLaunchers, rockets: Rockets):
    for rocket_launcher in rocket_launchers.elements:
        if rocket_launcher.STATE == RocketLauncher.STATE_INIT:
            rocket_launcher.y = rocket_launcher.y + rocket_launcher.speed / 40
            if rocket_launcher.y >= 50:
                rocket_launcher.STATE = RocketLauncher.STATE_MOVE
                trying = True
                while trying:
                    rocket_launcher.dest_x = random.randint((0 + RocketLauncher.width // 2), context.width - RocketLauncher.width // 2)
                    rocket_launcher.dest_y = random.randint(0 + RocketLauncher.height // 2, context.height - RocketLauncher.height // 2)
                    leng = length(player.x, rocket_launcher.dest_x, player.y, rocket_launcher.dest_y)
                    if leng >= 600:
                        trying = False
                        rocket_launcher.start_time = context.time
                        rocket_launcher.x_0, rocket_launcher.y_0 = rocket_launcher.x, rocket_launcher.y
                        rocket_launcher.dir_x, rocket_launcher.dir_y = get_direction(rocket_launcher.x_0, rocket_launcher.y_0, rocket_launcher.dest_x, rocket_launcher.dest_y)
                        rocket_launcher.time = random.randint(1, 4)
        if rocket_launcher.STATE == RocketLauncher.STATE_MOVE:
            d_t = context.time - rocket_launcher.start_time
            if d_t < rocket_launcher.time:
                rocket_launcher.x = rocket_launcher.x_0 + rocket_launcher.dir_x * d_t * rocket_launcher.speed
                rocket_launcher.y = rocket_launcher.y_0 + rocket_launcher.dir_y * d_t * rocket_launcher.speed
            else:
                rocket_launcher.STATE = RocketLauncher.STATE_WAIT
                rocket_launcher.start_time = context.time
                rocket_launcher.time = random.randint(1, 4)
        if rocket_launcher.STATE == RocketLauncher.STATE_WAIT:
            if context.time - rocket_launcher.start_time >= rocket_launcher.time:
                rocket_launcher.STATE = RocketLauncher.STATE_SHOOT
        if rocket_launcher.STATE == RocketLauncher.STATE_SHOOT:
            spawn_rockets(rockets, rocket_launcher.x, rocket_launcher.y, "enemy")
            rocket_launcher.STATE = RocketLauncher.STATE_INIT
        if rocket_launcher.health <= 0:
            rocket_launcher.STATE = RocketLauncher.STATE_KILL


def control_rockets(rockets: Rockets, context: PygameContext, player: Player):
    for rocket in rockets.elements:
        if rocket.state == Rocket.STATE_MOVE:
            rocket.dest_x = player.x
            rocket.dest_y = player.y
            rocket.dir_x, rocket.dir_y = get_direction(rocket.x, rocket.y, rocket.dest_x, rocket.dest_y)
            rocket.x = rocket.x + rocket.dir_x * rocket.speed
            rocket.y = rocket.y + rocket.dir_y * rocket.speed
        if rocket.health <= 0:
            rocket.state = Rocket.STATE_DESTROY


def control(context: PygameContext, player: Player, runners: Runners, bullets: Bullets, bullet_shooters: BulletShooters, rocket_launchers: RocketLaunchers, rockets: Rockets):
    control_runners(context, player, runners, bullets)
    bullet_shooters.control(context, player, bullets)
    control_rocket_launchers(context, player, rocket_launchers, rockets)
    control_bullets(bullets, context, runners)
    control_rockets(rockets, context, player)


def contacts(context: PygameContext, player: Player, runners: Runners, bullets: Bullets, bullet_shooters: BulletShooters, rockets: Rockets, rocket_launchers: RocketLaunchers):
    for runner in runners.elements:
        if runner.r.colliderect(player.r) and not runner.wounded:
            player.health = player.health - 1
            runner.wounded = True
        for bullet in bullets.elements:
            if runner.r.colliderect(bullet.form) and bullet.attacker == "friend":
                runner.health = runner.health - 1
                bullet.sharp = False

        tmp_list = []
        for x in runners.elements:
            if x.state != Runner.STATE_KILLED:
                tmp_list.append(x)
        runners.elements = tmp_list

    bullet_shooters.contacts(context, bullets)

    for bullet in bullets.elements:
        if bullet.form.colliderect(player.r) and bullet.attacker == "enemy":
            player.health = player.health - 1
            bullet.sharp = False
        for rocket in rockets.elements:
            if bullet.form.colliderect(rocket.form) and bullet.attacker == "friend":
                bullet.sharp = False
                rocket.health = rocket.health - 1
        for rocket_launcher in rocket_launchers.elements:
            if bullet.form.colliderect(rocket_launcher.form) and bullet.attacker == "friend":
                bullet.sharp = False
                rocket_launcher.health = rocket_launcher.health - 1

    for rocket_launcher in rocket_launchers.elements:
        tmp_list = []
        for x in rocket_launchers.elements:
            if not x.STATE == RocketLauncher.STATE_KILL:
                tmp_list.append(x)
        rocket_launchers.elements = tmp_list

    for rocket in rockets.elements:
        if rocket.form.colliderect(player.r):
            rocket.state = Rocket.STATE_DESTROY
            player.health = player.health - 1

    for rocket in rockets.elements:
        tmp_list = []
        for x in rockets.elements:
            if not x.state == Rocket.STATE_DESTROY:
                tmp_list.append(x)
        rockets.elements = tmp_list

    for bullet in bullets.elements:
        tmp_list = []
        for x in bullets.elements:
            if not x.sharp == False:
                tmp_list.append(x)
        bullets.elements = tmp_list


def player_picture(player: Player, context: PygameContext):
    player.form = player.pictures[player.health - 1]
    context.screen.blit(player.form, player.r)


def draw_player(context: PygameContext, player: Player):
    player.r = pygame.Rect(player.x - player.width / 2, player.y - player.height / 2, player.width, player.height)
    #player.form = pygame.draw.rect(context.screen, (255, 255, 255), player.r)
    player_picture(player, context)


def draw_bullets(context: PygameContext, bullets: Bullets):
    for bullet in bullets.elements:
        if bullet.attacker == "friend":
            bullet.form = context.screen.blit(bullet.forms[0], (bullet.x, bullet.y))
        else:
            bullet.form = pygame.draw.circle(context.screen, (255, 0, 0), (bullet.x, bullet.y), bullet.r)


def draw_mouse(context: PygameContext):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pygame.draw.circle(context.screen, (255, 255, 255), (mouse_x, mouse_y), 10)


def draw_runners(context: PygameContext, runners: Runners):
    for runner in runners.elements:
        runner.r = pygame.Rect(runner.x - runner.width / 2, runner.y - runner.height / 2, runner.width, runner.height)
        runner.form = pygame.draw.rect(context.screen, (0, 255, 0), runner.r)


def draw_rocket_launchers(context: PygameContext, rocket_launchers: RocketLaunchers):
    for rocket_launcher in rocket_launchers.elements:
        r = pygame.Rect(rocket_launcher.x - rocket_launcher.width / 2, rocket_launcher.y - rocket_launcher.height / 2, rocket_launcher.width, rocket_launcher.height)
        rocket_launcher.form = pygame.draw.rect(context.screen, (200, 200, 200), r)


def draw_rockets(context: PygameContext, rockets: Rockets):
    for rocket in rockets.elements:
        r = pygame.Rect(rocket.x - rocket.width / 2, rocket.y - rocket.height / 2, rocket.width, rocket.height)
        rocket.form = pygame.draw.rect(context.screen, (230, 0, 100), r)


def draw(context: PygameContext, player: Player, runners: Runners, bullets: Bullets, bullet_shooters: BulletShooters, rocket_launchers: RocketLaunchers, rockets: Rockets):
    context.screen.fill((0, 0, 0))

    draw_player(context, player)
    draw_mouse(context)
    draw_bullets(context, bullets)
    bullet_shooters.draw(context)
    draw_runners(context, runners)
    draw_rocket_launchers(context, rocket_launchers)
    draw_rockets(context, rockets)

    pygame.display.flip()


def game_logic(game_logic_parameters: GameLogic, context: PygameContext, player: Player, bullet_shooters: BulletShooters, runners: Runners, rocket_launchers: RocketLaunchers):
    if game_logic_parameters.wave_time == 0:
        for i in range(4):
            bullet_shooters.spawn(context)
    if bullet_shooters.empty() and game_logic_parameters.wave == 1:
        game_logic_parameters.wave_time = 1200

    if game_logic_parameters.wave_time == 1200:
        game_logic_parameters.wave = game_logic_parameters.wave + 1
        for i in range(6):
            bullet_shooters.spawn(context)
        for i in range(2):
            spawn_runners(context, player, runners)
    if bullet_shooters.empty() and len(runners.elements) == 0 and game_logic_parameters.wave == 2:
        game_logic_parameters.wave_time = 3600

    if game_logic_parameters.wave_time == 3600:
        game_logic_parameters.wave = game_logic_parameters.wave + 1
        for i in range(4):
            bullet_shooters.spawn(context)
            spawn_runners(context, player, runners)
    if bullet_shooters.empty() and len(runners.elements) == 0 and game_logic_parameters.wave == 3:
        game_logic_parameters.wave_time = 6000

    if game_logic_parameters.wave_time == 6000:
        game_logic_parameters.wave = game_logic_parameters.wave + 1
        for i in range(8):
            spawn_runners(context, player, runners)
    if len(runners.elements) == 0 and game_logic_parameters.wave == 4:
        game_logic_parameters.wave_time = 9000

    if game_logic_parameters.wave_time == 9000:
        game_logic_parameters.wave = game_logic_parameters.wave + 1
        for i in range(4):
            bullet_shooters.spawn(context)
        for i in range(2):
            spawn_rocket_launchers(context, player, rocket_launchers)
    if bullet_shooters.empty() and len(rocket_launchers.elements) == 0 and game_logic_parameters.wave == 5:
        game_logic_parameters.wave_time = 11000

    if game_logic_parameters.wave_time == 11000:
        game_logic_parameters.wave = game_logic_parameters.wave + 1
        for i in range(3):
            bullet_shooters.spawn(context)
            spawn_rocket_launchers(context, player, rocket_launchers)
        for i in range(2):
            spawn_runners(context, player, runners)
    if bullet_shooters.empty() and len(rocket_launchers.elements) == 0 and len(runners.elements) == 0 and game_logic_parameters.wave == 6:
        game_logic_parameters.wave_time = 14000

    if game_logic_parameters.wave_time == 14000:
        game_logic_parameters.wave = game_logic_parameters.wave + 1
        for i in range(3):
            spawn_rocket_launchers(context, player, rocket_launchers)
            spawn_runners(context, player, runners)
        for i in range(4):
            bullet_shooters.spawn(context)

    game_logic_parameters.wave_time = game_logic_parameters.wave_time + 1


def game(context: PygameContext):
    player = Player(context.width // 2, context.height // 2)

    game_logic_parameters = GameLogic()

    bullets = Bullets()
    rockets = Rockets()
    runners = Runners()
    bullet_shooters = BulletShooters()
    rocket_launchers = RocketLaunchers()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                press_mouse(running, bullets, player, context, bullet_shooters)

        #keys = pygame.key.get_pressed()
        #if keys[pygame.K_ESCAPE]:
        #    menu(True)

        running = control_player(context, player, running)
        control(context, player, runners, bullets, bullet_shooters, rocket_launchers, rockets)
        draw(context, player, runners, bullets, bullet_shooters, rocket_launchers, rockets)
        contacts(context, player, runners, bullets, bullet_shooters, rockets, rocket_launchers)
        game_logic(game_logic_parameters, context, player, bullet_shooters, runners, rocket_launchers)

        context.delta_time = context.clock.tick(60) / 1000
        context.time = context.time + context.delta_time
