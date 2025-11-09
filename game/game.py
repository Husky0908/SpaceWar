import pygame
from base.context import PygameContext
from base.bullets import Bullets
from base.player import Player
from enemies.bullet_shooters import BulletShooters
from enemies.runners import Runners
from base.rockets import Rockets
from enemies.rocket_launchers import RocketLaunchers
from enemies.first_boss import FirstBoss
from game.game_logic import GameLogic
from texts.options_save import OptionsSave
from menu.menu import menu
from texts.text_print import print_text
from base.boxes import Coins, PlusHealths, Upgraders
from enemies.supermacy import Supermacys


class Game:
    def __init__(self):
        self.running = True
        self.end = False
        self.end_text = None
        self.end_time = 0

    def control(self, context: PygameContext, player: Player, runners: Runners, bullets: Bullets, bullet_shooters: BulletShooters, rocket_launchers: RocketLaunchers, rockets: Rockets, first_boss: FirstBoss, coins: Coins, plus_hp: PlusHealths, upgrades: Upgraders, supermacys: Supermacys):
        runners.control(context, player, coins, plus_hp)
        bullet_shooters.control(context, player, bullets, coins)
        rocket_launchers.control(context, player, rockets, plus_hp, coins)
        supermacys.control(player, bullet_shooters, bullets)
        first_boss.control(context, player, bullets, upgrades)
        bullets.control(context)
        rockets.control(player)

        coins.control(context)
        plus_hp.control(context)
        upgrades.control(context)

    def contacts(self, context: PygameContext, player: Player, runners: Runners, bullets: Bullets, bullet_shooters: BulletShooters, rockets: Rockets, rocket_launchers: RocketLaunchers, first_boss: FirstBoss, coins: Coins, plus_hp: PlusHealths, upgrades: Upgraders, supermacys: Supermacys):

        runners.contacts(player, bullets)
        bullet_shooters.contacts(context, bullets)
        player.contacts(bullets, coins, plus_hp, upgrades)
        first_boss.contacts(bullets, player)
        rocket_launchers.contacts(bullets)
        supermacys.contacts(bullets)

        for bullet in bullets.elements:

            for rocket in rockets.elements:
                if bullet.form.colliderect(rocket.form) and bullet.attacker == "friend":
                    bullet.sharp = False
                    rocket.health = rocket.health - 1

        rockets.contacts(player)
        bullets.contacts()

    def draw_mouse(self, context: PygameContext, player: Player):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        context.screen.blit(player.crosshair_form, (mouse_x, mouse_y))

    def draw(self, context: PygameContext, player: Player, runners: Runners, bullets: Bullets, bullet_shooters: BulletShooters, rocket_launchers: RocketLaunchers, rockets: Rockets, first_boss: FirstBoss, options_saving: OptionsSave, coins: Coins, plus_hp: PlusHealths, game_logic_parameters: GameLogic, upgrades: Upgraders, supermacys: Supermacys):
        context.screen.fill((0, 0, 0))

        plus_hp.draw(context)
        coins.draw(context)
        upgrades.draw(context)

        bullet_shooters.draw(context)
        runners.draw(context)
        rocket_launchers.draw(context)
        supermacys.draw(context)
        first_boss.draw(context, player.dif)
        player.draw(context)
        bullets.draw(context)
        rockets.draw(context)
        self.draw_mouse(context, player)

        if self.end:
            if self.end_text == "Victory" or self.end_text == "Győzelem":
                print_text("23", 20, (255, 0, 0), ((context.width / 4 * 3), (context.height / 4 * 3)), context)
            print_text(self.end_text, 100, (255, 255, 255), ((context.width / 2), (context.height / 2)), context)
        elif game_logic_parameters.wave == 10:
            print_text(f"{(options_saving.languages[options_saving.select_language])["end"]} {str(10 - game_logic_parameters.wave_time // 60)}", 50, (255, 255, 255), (context.width / 2, 50), context)

        pygame.display.flip()

    def get_char(self, event: pygame.event.Event):
        if event.type == pygame.KEYUP:
            return event.key
        return None

    def game(self, context: PygameContext, options_saving: OptionsSave, name):
        player = Player(context.width // 2, context.height // 2, name)
        first_boss = FirstBoss(0, -350, player.dif)

        game_logic_parameters = GameLogic(player.dif, player.level)

        bullets = Bullets(context)
        rockets = Rockets()
        runners = Runners()
        bullet_shooters = BulletShooters()
        rocket_launchers = RocketLaunchers()
        supermacys = Supermacys()

        coins = Coins()
        plus_hp = PlusHealths()
        upgrades = Upgraders()

        self.running = True
        self.end = False
        cheat_mode = False
        cheat = ""
        input_timeout = 0
        show_menu = False

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass

                if cheat_mode and input_timeout == 0:
                    c = self.get_char(event)
                    if c == pygame.K_BACKSPACE:
                        cheat_mode = False
                    if c is not None:
                        cheat = cheat + chr(c)

                if not cheat_mode and event.type == pygame.KEYUP and event.unicode == chr(pygame.K_m):
                    cheat_mode = True
                    cheat = ""
                if event.type == pygame.KEYUP and event.unicode == chr(pygame.K_ESCAPE):
                    show_menu = True

            if show_menu:
                game_next = menu(context, options_saving, True, False, "")
                show_menu = False
                if game_next:
                    player.health = 0
                    player.write_player_text()
                    self.end = True
                    self.end_text = ""

            if not cheat_mode:
                context.time = context.time + context.delta_time

                if not self.end:
                    self.end = player.control(context, self.end, options_saving, bullets)
                    if self.end:
                        self.end_time = context.time
                        self.end_text = (options_saving.languages[options_saving.select_language])["game over"]
                        first_boss.live = False
                    if not self.end:
                        self.control(context, player, runners, bullets, bullet_shooters, rocket_launchers, rockets, first_boss, coins, plus_hp, upgrades, supermacys)
                        self.end = game_logic_parameters.wave_logic(context, bullet_shooters, runners, rocket_launchers, first_boss, supermacys)
                        if self.end:
                            self.end_time = context.time
                            self.end_text = (options_saving.languages[options_saving.select_language])["victory"]
                            if player.level == player.unlock_levels:
                                player.unlock_levels = player.unlock_levels + 1
                            player.write_player_text()
                            player.health = 0
                    self.draw(context, player, runners, bullets, bullet_shooters, rocket_launchers, rockets, first_boss, options_saving, coins, plus_hp, game_logic_parameters, upgrades, supermacys)
                    self.contacts(context, player, runners, bullets, bullet_shooters, rockets, rocket_launchers, first_boss, coins, plus_hp, upgrades, supermacys)
                else:
                    self.draw(context, player, runners, bullets, bullet_shooters, rocket_launchers, rockets, first_boss, options_saving, coins, plus_hp, game_logic_parameters, upgrades, supermacys)
                    bullets.elements.clear()
                    rockets.elements.clear()
                    runners.elements.clear()
                    bullet_shooters._elements.clear()
                    rocket_launchers.elements.clear()
                    coins.elements = []
                    plus_hp.elements = []
                    upgrades.elements = []
                    if context.time - self.end_time > 3 or self.end_text == "":
                        self.running = False

            else:
                if cheat == "megh":
                    player.health = 100
                    cheat_mode = False
                if cheat == "maxh":
                    player.health = 5
                    cheat_mode = False
                if cheat == "spo1b":
                    bullets.elements.clear()
                    rockets.elements.clear()
                    runners.elements.clear()
                    bullet_shooters._elements.clear()
                    rocket_launchers.elements.clear()

                    game_logic_parameters.wave_time = 16000
                    game_logic_parameters.wave = 8
                    cheat_mode = False
                if cheat == "joiar":
                    bullets.elements.clear()
                    rockets.elements.clear()
                    runners.elements.clear()
                    bullet_shooters._elements.clear()
                    rocket_launchers.elements.clear()
                    game_logic_parameters.level = 0
                    cheat_mode = False
                if cheat == "arerl":
                    for i in range(5):
                        rocket_launchers.spawn(context)
                    cheat_mode = False
                if cheat == "arebs":
                    for i in range(5):
                        bullet_shooters.spawn(context)
                    cheat_mode = False
                if cheat == "areru":
                    for i in range(5):
                        runners.spawn(context)
                    cheat_mode = False

            context.delta_time = context.clock.tick(60) / 1000

        return player.name
            
