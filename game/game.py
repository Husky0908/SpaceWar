import pygame
from base.context import PygameContext
from base.bullets import Bullets, Bullet
from base.player import Player
from enemies.bullet_shooters import BulletShooters
from enemies.runners import Runners
from base.rockets import Rocket, Rockets
from enemies.rocket_launchers import RocketLaunchers, RocketLauncher
from enemies.first_boss import FirstBoss
from texts.inputs import TextInput


class GameLogic:
    def __init__(self):
        self.level = 1
        self.wave_time = 0
        self.wave = 1


def control(context: PygameContext, player: Player, runners: Runners, bullets: Bullets, bullet_shooters: BulletShooters, rocket_launchers: RocketLaunchers, rockets: Rockets, first_boss: FirstBoss):
    runners.control(context, player)
    bullet_shooters.control(context, player, bullets)
    rocket_launchers.control(context, player, rockets)
    first_boss.control(context, player, bullets)
    bullets.control(context)
    rockets.control(player)


def contacts(context: PygameContext, player: Player, runners: Runners, bullets: Bullets, bullet_shooters: BulletShooters, rockets: Rockets, rocket_launchers: RocketLaunchers, first_boss: FirstBoss):

    runners.contacts(player, bullets)
    bullet_shooters.contacts(context, bullets)
    player.contacts(bullets)
    first_boss.contacts(bullets, player)

    for bullet in bullets.elements:

        rocket_launchers.contacts(bullet)

        for rocket in rockets.elements:
            if bullet.form.colliderect(rocket.form) and bullet.attacker == "friend":
                bullet.sharp = False
                rocket.health = rocket.health - 1

    rockets.contacts(player)
    bullets.contacts()


def draw_mouse(context: PygameContext, player: Player):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    #pygame.draw.circle(context.screen, (255, 255, 255), (mouse_x, mouse_y), 10)
    context.screen.blit(player.crosshair_form, (mouse_x, mouse_y))

def draw(context: PygameContext, player: Player, runners: Runners, bullets: Bullets, bullet_shooters: BulletShooters, rocket_launchers: RocketLaunchers, rockets: Rockets, first_boss: FirstBoss):
    context.screen.fill((0, 0, 0))

    bullets.draw(context)
    bullet_shooters.draw(context)
    runners.draw(context)
    rocket_launchers.draw(context)
    rockets.draw(context)
    first_boss.draw(context)
    player.draw(context)
    draw_mouse(context, player)

    pygame.display.flip()


def game_logic(game_logic_parameters: GameLogic, context: PygameContext, player: Player, bullet_shooters: BulletShooters, runners: Runners, rocket_launchers: RocketLaunchers, first_boss: FirstBoss):
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
    if bullet_shooters.empty() and len(rocket_launchers.elements) == 0 and len(runners.elements) == 0 and game_logic_parameters.wave == 7:
        game_logic_parameters.wave = game_logic_parameters.wave + 1

    if game_logic_parameters.wave == 8:
        first_boss.spawn()
        game_logic_parameters.wave = 9

    game_logic_parameters.wave_time = game_logic_parameters.wave_time + 1


def game(context: PygameContext):
    player = Player(context.width // 2, context.height // 2)
    first_boss = FirstBoss(0, -350)

    t_input = TextInput()

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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            t_input.input_player(context)
        #if keys[pygame.K_ESCAPE]:
        #    menu(True)

        running = player.control(context, running)
        control(context, player, runners, bullets, bullet_shooters, rocket_launchers, rockets, first_boss)
        draw(context, player, runners, bullets, bullet_shooters, rocket_launchers, rockets, first_boss)
        contacts(context, player, runners, bullets, bullet_shooters, rockets, rocket_launchers, first_boss)
        game_logic(game_logic_parameters, context, player, bullet_shooters, runners, rocket_launchers, first_boss)

        context.delta_time = context.clock.tick(60) / 1000
        context.time = context.time + context.delta_time
