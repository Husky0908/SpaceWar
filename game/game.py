import pygame
from base.context import PygameContext
from base.bullets import Bullets, Bullet
from base.player import Player
from enemies.bullet_shooters import BulletShooters
from enemies.runners import Runners
from base.rockets import Rocket, Rockets
from enemies.rocket_launchers import RocketLaunchers, RocketLauncher
from enemies.first_boss import FirstBoss
from game.game_logic import GameLogic
from texts.options_save import OptionsSave


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


def get_char(event: pygame.event) -> int:
    if event.type == pygame.KEYUP:
        return event.key
    return None
    


def game(context: PygameContext, options_saving: OptionsSave):
    player = Player(context.width // 2, context.height // 2)
    first_boss = FirstBoss(0, -350)

    game_logic_parameters = GameLogic(options_saving.game_difficulty)

    bullets = Bullets()
    rockets = Rockets()
    runners = Runners()
    bullet_shooters = BulletShooters()
    rocket_launchers = RocketLaunchers()

    running = True
    cheat_mode = False
    input_timeout = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.press_mouse(running, bullets, context)

            if cheat_mode and input_timeout == 0:
                c = get_char(event)
                if c == pygame.K_ESCAPE:
                    cheat_mode = False
                if c is not None:
                    cheat = cheat + chr(c)


            if not cheat_mode and event.type == pygame.KEYUP and event.unicode == chr(pygame.K_m):
                cheat_mode = True
                cheat = ""
                
        #if keys[pygame.K_ESCAPE]:
        #    menu(True)
        

        if not cheat_mode:
            context.time = context.time + context.delta_time
            
            running = player.control(context, running)
            control(context, player, runners, bullets, bullet_shooters, rocket_launchers, rockets, first_boss)
            draw(context, player, runners, bullets, bullet_shooters, rocket_launchers, rockets, first_boss)
            contacts(context, player, runners, bullets, bullet_shooters, rockets, rocket_launchers, first_boss)
            game_logic_parameters.wave_logic(context, bullet_shooters, runners, rocket_launchers, first_boss)
        else:
            if cheat == "iddqd":
                player.health = 5
                cheat_mode = False
            if cheat == "idkfa":
                bullets.elements.clear()
                rockets.elements.clear()
                runners.elements.clear()
                bullet_shooters._elements.clear()
                rocket_launchers.elements.clear()
                
                game_logic_parameters.wave_time = 16000
                game_logic_parameters.wave = 8
                cheat_mode = False


        context.delta_time = context.clock.tick(60) / 1000

