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
from game.game_logic import GameLogic


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
        game_logic_parameters.wave_logic(context, bullet_shooters, runners, rocket_launchers, first_boss)

        context.delta_time = context.clock.tick(60) / 1000
        context.time = context.time + context.delta_time
