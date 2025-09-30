import pygame
from base.context import PygameContext
from texts.text_print import print_text
from texts.options_save import OptionsSave
from base.directions import get_direction


class Map_and_Upgrades:
    def __init__(self, ship_name: str):
        self.how_many_map = 1
        self.how_many_map_now = 1
        self.ship_name = ship_name
        with (open(f"texts/players/{self.ship_name}", "r") as f):
            self.difficulty = int(f.readline().strip("\n"))
            self.hmm = int(f.readline().strip("\n"))
            self.hmmu = int(f.readline().strip("\n"))
            self.coin = int(f.readline().strip("\n"))
            self.upgrade_box = int(f.readline().strip("\n"))
            self.ship_def = int(f.readline().strip("\n"))
            self.mas_gun = int(f.readline().strip("\n"))
            self.bomb = int(f.readline().strip("\n"))
            self.rocket = int(f.readline().strip("\n"))
            self.skins = int(f.readline().strip("\n"))
        self.map_picture = pygame.image.load("Pictures/menu_pictures/map.png").convert_alpha()
        self.map_background = pygame.image.load("Pictures/menu_pictures/map_background.png").convert_alpha()
        self.lock_picture = pygame.image.load("Pictures/menu_pictures/lock.png").convert_alpha()
        self.complete_picture = pygame.image.load("Pictures/menu_pictures/complete.png").convert_alpha()
        self.upgrade_ship = pygame.image.load("Pictures/menu_pictures/upgrade_ship.png").convert_alpha()
        self.coin_picture = pygame.image.load("Pictures/other_pictures/coin.png").convert_alpha()
        self.upgrader_box_picture = pygame.image.load("Pictures/other_pictures/upgrader_box.png").convert_alpha()
        self.button_plate = pygame.image.load("Pictures/menu_pictures/button_plate.png").convert_alpha()
        self.button_plate_on = pygame.image.load("Pictures/menu_pictures/button_plate_on.png").convert_alpha()
        self.dir_x = 0
        self.dir_y = 0
        self.start_time = 0
        self.time = 0
        self.x_0 = 55
        self.y_0 = 545
        self.x = 55
        self.y = 545
        self.move = False

    def map(self, context: PygameContext, mouse_form, mouse_click, mouse_click_time, options_save: OptionsSave, ship):
        first_mission = pygame.draw.rect(context.screen, (255, 255, 255), (55, 545, 80, 80))
        second_mission = pygame.draw.rect(context.screen, (255, 255, 255), (200, 370, 80, 80))
        context.screen.blit(self.map_background, (0, 0))
        context.screen.blit(self.map_picture, (-10, 0))
        if self.hmmu < 8:
            context.screen.blit(self.lock_picture, (1125, 465))
            if self.hmmu < 7:
                context.screen.blit(self.lock_picture, (950, 355))
                if self.hmmu < 6:
                    context.screen.blit(self.lock_picture, (810, 285))
                    if self.hmmu < 5:
                        context.screen.blit(self.lock_picture, (670, 385))
                        if self.hmmu < 4:
                            context.screen.blit(self.lock_picture, (590, 490))
                            if self.hmmu < 3:
                                context.screen.blit(self.lock_picture, (425, 375))
                                if self.hmmu < 2:
                                    context.screen.blit(self.lock_picture, (210, 385))
        if self.hmmu > 1:
            context.screen.blit(self.complete_picture, (70, 450))
        context.screen.blit(ship, (self.x, self.y))
        print_text(self.ship_name, 60, (255, 255, 255), (175, 70), context)
        start_button = pygame.draw.rect(context.screen, (255, 255, 255), ((context.width / 4 * 2 + 110), 625, 200, 80))
        print_text((options_save.languages[options_save.select_language])["start"], 45, (0, 0, 0), ((context.width / 4 * 2 + 210), 665), context)
        go_upgrade = context.screen.blit(self.button_plate, (context.width / 4 * 3 + 60, 50))
        print_text((options_save.languages[options_save.select_language])["upgrades"], 45, (255, 255, 255), ((1280 / 4 * 3 + 175), 130), context)
        back_main_menu = context.screen.blit(self.button_plate, (context.width / 4 * 3 + 60, 590))
        print_text((options_save.languages[options_save.select_language])["back"], 45, (255, 255, 255), ((1280 / 4 * 3 + 175), 670), context)

        if back_main_menu.colliderect(mouse_form):
            context.screen.blit(self.button_plate_on, (context.width / 4 * 3 + 60, 590))
            print_text((options_save.languages[options_save.select_language])["back"], 45, (255, 255, 255), ((1280 / 4 * 3 + 180), 675), context)
        if go_upgrade.colliderect(mouse_form):
            context.screen.blit(self.button_plate_on, (context.width / 4 * 3 + 60, 50))
            print_text((options_save.languages[options_save.select_language])["upgrades"], 45, (255, 255, 255), ((1280 / 4 * 3 + 180), 135), context)
        if start_button.colliderect(mouse_form):
            context.screen.blit(ship, ((1280 / 4 * 2 + 45), 625))

        if first_mission.colliderect(mouse_form) and mouse_click and not self.how_many_map == 1 and not self.how_many_map_now == 1.5:
            self.how_many_map = 1
            self.move = True
            self.get_direction_map()
        if second_mission.colliderect(mouse_form) and mouse_click and not self.how_many_map == 2 and self.hmmu >= 2 and not self.how_many_map_now == 1.5:
            self.how_many_map = 2
            self.move = True
            self.get_direction_map()
            
        if self.move:
            d_t = self.time - self.start_time
            if d_t < 47:
                self.x = self.x_0 + self.dir_x * d_t * 5
                self.y = self.y_0 + self.dir_y * d_t * 5
            else:
                if self.how_many_map == 2:
                    self.how_many_map_now = 2
                else:
                    self.how_many_map_now = 1
                self.move = False
                self.start_time = self.time

        self.time = self.time + 1

        if (start_button.colliderect(mouse_form) and mouse_click and self.how_many_map_now == 1) or (first_mission.colliderect(mouse_form) and mouse_click and self.how_many_map_now == 1):
            return "play the game", mouse_click_time
        if go_upgrade.colliderect(mouse_form) and mouse_click and mouse_click_time >= 15:
            mouse_click_time = 0
            return "upgrade", mouse_click_time
        if back_main_menu.colliderect(mouse_form) and mouse_click:
            return "main menu", mouse_click_time
        else:
            return "map", mouse_click_time
        
    def upgrade(self, context: PygameContext, mouse_form, mouse_click, mouse_press_time, options_save: OptionsSave, ship):
        print_text(self.ship_name, 60, (255, 255, 255), (175, 70), context)
        go_map = context.screen.blit(self.button_plate, (context.width / 4 * 3 + 60, 50))
        print_text((options_save.languages[options_save.select_language])["map"], 45, (255, 255, 255), ((1280 / 4 * 3 + 175), 130), context)
        back_main_menu = context.screen.blit(self.button_plate, (context.width / 4 * 3 + 60, 590))
        print_text((options_save.languages[options_save.select_language])["back"], 45, (255, 255, 255), ((1280 / 4 * 3 + 175), 670), context)

        context.screen.blit(self.upgrade_ship, (context.width / 2 - 200, context.height / 2 - 200))
        context.screen.blit(self.coin_picture, (context.width / 2 - 200, 50))
        print_text(str(self.coin), 45, (255, 255, 255), (context.width / 2 - 120, 80), context)
        context.screen.blit(self.upgrader_box_picture, (context.width / 2 + 50, 50))
        print_text(str(self.upgrade_box), 45, (255, 255, 255), (context.width / 2 + 150, 80), context)
        print_text((options_save.languages[options_save.select_language])["machine gun"], 45, (255, 255, 255), (context.width / 4, context.height / 4 * 3 - 50), context)
        print_text((options_save.languages[options_save.select_language])["level"] + " " + str(self.mas_gun), 45, (255, 255, 255), (context.width / 4, context.height / 4 * 3), context)
        mas_gun_upgrade_button = pygame.draw.rect(context.screen, (255, 255, 255), (context.width / 4 - 100, context.height / 4 * 3 + 40, 200, 80))
        if self.mas_gun == 1:
            context.screen.blit(self.coin_picture, (context.width / 4 - 60, context.height / 4 * 3 + 55))
            print_text("200", 45, (0, 0, 0), (context.width / 4 + 20, context.height / 4 * 3 + 80), context)
        if self.mas_gun == 2:
            print_text("Max", 45, (0, 0, 0), (context.width / 4, context.height / 4 * 3 + 80), context)

        if mas_gun_upgrade_button.colliderect(mouse_form) and mouse_click and self.mas_gun == 1 and self.coin >= 200:
            self.mas_gun = 2
            self.coin = self.coin - 200
            self.write_file()
            
        if back_main_menu.colliderect(mouse_form):
            context.screen.blit(self.button_plate_on, (context.width / 4 * 3 + 60, 590))
            print_text((options_save.languages[options_save.select_language])["back"], 45, (255, 255, 255), ((1280 / 4 * 3 + 180), 675), context)
        if go_map.colliderect(mouse_form):
            context.screen.blit(self.button_plate_on, (context.width / 4 * 3 + 60, 50))
            print_text((options_save.languages[options_save.select_language])["map"], 45, (255, 255, 255), ((1280 / 4 * 3 + 180), 135), context)

        if back_main_menu.colliderect(mouse_form) and mouse_click:
            return "main menu", mouse_press_time
        if go_map.colliderect(mouse_form) and mouse_click and mouse_press_time >= 15:
            mouse_press_time = 0
            return "map", mouse_press_time
        else:
            return "upgrade", mouse_press_time
        
    def write_file(self):
        with open(f"texts/players/{self.ship_name}", "w") as f:
            f.write(f"{self.difficulty}\n")
            f.write(f"{self.hmm}\n")
            f.write(f"{self.hmmu}\n")
            f.write(f"{self.coin}\n")
            f.write(f"{self.upgrade_box}\n")
            f.write(f"{self.ship_def}\n")
            f.write(f"{self.mas_gun}\n")
            f.write(f"{self.bomb}\n")
            f.write(f"{self.rocket}\n")
            f.write(f"{self.skins}\n")
        
    def get_direction_map(self):
        if self.how_many_map == 2:
            self.dir_x, self.dir_y = get_direction(55, 545, 200, 370)
            self.x_0, self.y_0 = 55, 545
        else:
            self.dir_x, self.dir_y = get_direction(201, 367, 55, 545)
            self.x_0, self.y_0 = 201, 367
        self.how_many_map_now = 1.5
        self.start_time = self.time
            
