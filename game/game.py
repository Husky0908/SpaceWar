import pygame
from base.context import PygameContext
from base.bullets import Bullets, Bullet
from base.player import Player
from enemies.bullet_shooters import BulletShooters
from enemies.runners import Runners
from base.directions import get_direction, length
from base.rockets import Rocket, Rockets
from enemies.rocket_launchers import RocketLaunchers, RocketLauncher


class GameLogic:
    def __init__(self):
        self.level = 1
        self.wave_time = 0
        self.wave = 1


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
    runners.control(context, player)
    bullet_shooters.control(context, player, bullets)
    rocket_launchers.control(context, player, rockets)
    bullets.control(context)
    control_rockets(rockets, context, player)


def contacts(context: PygameContext, player: Player, runners: Runners, bullets: Bullets, bullet_shooters: BulletShooters, rockets: Rockets, rocket_launchers: RocketLaunchers):

    runners.contacts(player, bullets)
    bullet_shooters.contacts(context, bullets)
    player.contacts(bullets, rockets)

    for bullet in bullets.elements:
        for rocket in rockets.elements:
            if bullet.form.colliderect(rocket.form) and bullet.attacker == "friend":
                bullet.sharp = False
                rocket.health = rocket.health - 1
        rocket_launchers.contacts(bullet)

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


def draw_bullets(context: PygameContext, bullets: Bullets):
    for bullet in bullets.elements:
        if bullet.attacker == "friend":
            bullet.form = context.screen.blit(bullet.forms[0], (bullet.x, bullet.y))
        else:
            bullet.form = pygame.draw.circle(context.screen, (255, 0, 0), (bullet.x, bullet.y), bullet.r)


def draw_mouse(context: PygameContext):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pygame.draw.circle(context.screen, (255, 255, 255), (mouse_x, mouse_y), 10)


def draw_rockets(context: PygameContext, rockets: Rockets):
    for rocket in rockets.elements:
        r = pygame.Rect(rocket.x - rocket.width / 2, rocket.y - rocket.height / 2, rocket.width, rocket.height)
        rocket.form = pygame.draw.rect(context.screen, (230, 0, 100), r)


def draw(context: PygameContext, player: Player, runners: Runners, bullets: Bullets, bullet_shooters: BulletShooters, rocket_launchers: RocketLaunchers, rockets: Rockets):
    context.screen.fill((0, 0, 0))

    player.draw(context)
    draw_mouse(context)
    draw_bullets(context, bullets)
    bullet_shooters.draw(context)
    runners.draw(context)
    rocket_launchers.draw(context)
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
        for i in range(4):
            bullet_shooters.spawn(context)
        for i in range(2):
            runners.spawn(context)
    if bullet_shooters.empty() and len(runners.elements) == 0 and game_logic_parameters.wave == 2:
        game_logic_parameters.wave_time = 3600

    if game_logic_parameters.wave_time == 3600:
        game_logic_parameters.wave = game_logic_parameters.wave + 1
        for i in range(4):
            bullet_shooters.spawn(context)
            runners.spawn(context)
    if bullet_shooters.empty() and len(runners.elements) == 0 and game_logic_parameters.wave == 3:
        game_logic_parameters.wave_time = 6000

    if game_logic_parameters.wave_time == 6000:
        game_logic_parameters.wave = game_logic_parameters.wave + 1
        for i in range(8):
            runners.spawn(context)
    if len(runners.elements) == 0 and game_logic_parameters.wave == 4:
        game_logic_parameters.wave_time = 9000

    if game_logic_parameters.wave_time == 9000:
        game_logic_parameters.wave = game_logic_parameters.wave + 1
        for i in range(4):
            bullet_shooters.spawn(context)
        for i in range(2):
            rocket_launchers.spawn(context)
    if bullet_shooters.empty() and len(rocket_launchers.elements) == 0 and game_logic_parameters.wave == 5:
        game_logic_parameters.wave_time = 11000

    if game_logic_parameters.wave_time == 11000:
        game_logic_parameters.wave = game_logic_parameters.wave + 1
        for i in range(3):
            bullet_shooters.spawn(context)
            rocket_launchers.spawn(context)
        for i in range(2):
            runners.spawn(context)
    if bullet_shooters.empty() and len(rocket_launchers.elements) == 0 and len(runners.elements) == 0 and game_logic_parameters.wave == 6:
        game_logic_parameters.wave_time = 14000

    if game_logic_parameters.wave_time == 14000:
        game_logic_parameters.wave = game_logic_parameters.wave + 1
        for i in range(3):
            rocket_launchers.spawn(context)
            runners.spawn(context)
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
                player.press_mouse(running, bullets, context)

        #keys = pygame.key.get_pressed()
        #if keys[pygame.K_ESCAPE]:
        #    menu(True)

        running = player.control(context, running)
        control(context, player, runners, bullets, bullet_shooters, rocket_launchers, rockets)
        draw(context, player, runners, bullets, bullet_shooters, rocket_launchers, rockets)
        contacts(context, player, runners, bullets, bullet_shooters, rockets, rocket_launchers)
        game_logic(game_logic_parameters, context, player, bullet_shooters, runners, rocket_launchers)

        context.delta_time = context.clock.tick(60) / 1000
        context.time = context.time + context.delta_time
