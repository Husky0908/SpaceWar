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
        self.upgrade_picture = pygame.image.load("Pictures/menu_pictures/upgrade.png").convert_alpha()
        self.upgrade_max_picture = pygame.image.load("Pictures/menu_pictures/upgrade_max.png").convert_alpha()
        self.easy_picture = pygame.image.load("Pictures/menu_pictures/easy.png").convert_alpha()
        self.normal_picture = pygame.image.load("Pictures/menu_pictures/normal.png").convert_alpha()
        self.hard_picture = pygame.image.load("Pictures/menu_pictures/hard.png").convert_alpha()
        self.dir_x = 0
        self.dir_y = 0
        self.start_time = 0
        self.time = 0
        self.x_0 = 55
        self.y_0 = 545
        self.x = 55
        self.y = 545
        self.move = False

    def map(self, context: PygameContext, mouse_form, mouse_button_state, options_save: OptionsSave, ship):
        first_mission = pygame.draw.rect(context.screen, (255, 255, 255), (55, 545, 80, 80))
        second_mission = pygame.draw.rect(context.screen, (255, 255, 255), (200, 370, 80, 80))
        third_mission = pygame.draw.rect(context.screen, (255, 255, 255), (410, 355, 80, 80))
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
        if self.hmmu > 2:
            context.screen.blit(self.complete_picture, (220, 280))
        context.screen.blit(ship, (self.x, self.y))
        print_text(self.ship_name, 60, (255, 255, 255), (175, 70), context)
        if self.difficulty == -1:
            context.screen.blit(self.easy_picture, (115, 100))
        if self.difficulty == 0:
            context.screen.blit(self.normal_picture, (115, 100))
        if self.difficulty == 1:
            context.screen.blit(self.hard_picture, (115, 100))
        start_button = context.screen.blit(self.button_plate, ((context.width / 4 * 2 + 110), 590))
        print_text((options_save.languages[options_save.select_language])["start"], 45, (255, 255, 255), ((context.width / 4 * 2 + 225), 670), context)
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
            context.screen.blit(self.button_plate_on, ((context.width / 4 * 2 + 110), 590))
            print_text((options_save.languages[options_save.select_language])["start"], 45, (255, 255, 255), ((context.width / 4 * 2 + 230), 675), context)

        keys = pygame.key.get_pressed()
        if ((first_mission.colliderect(mouse_form) and mouse_button_state == 1) or keys[options_save.left_control]) and not self.how_many_map == 1 and not self.how_many_map_now == 1.5:
            mouse_button_state = 2
            self.how_many_map = 1
            self.move = True
            self.get_direction_map()
        if ((second_mission.colliderect(mouse_form) and mouse_button_state == 1) or keys[options_save.right_control]) and not self.how_many_map == 2 and self.hmmu >= 2 and not self.how_many_map_now == 1.5:
            mouse_button_state = 2
            self.how_many_map = 2
            self.move = True
            self.get_direction_map()
        if keys[pygame.K_RETURN]:
            enter = True
        else:
            enter = False

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

        if (start_button.colliderect(mouse_form) and mouse_button_state == 1) or (first_mission.colliderect(mouse_form) and mouse_button_state == 1) or (second_mission.colliderect(mouse_form) and mouse_button_state == 1) or enter or (third_mission.colliderect(mouse_form) and mouse_button_state == 1):
            mouse_button_state = 2
            if self.how_many_map_now == 1:
                self.hmm = 1
            if self.how_many_map_now == 2:
                self.hmm = 2
            if third_mission.colliderect(mouse_form):
                self.hmm = 3
            self.write_file()
            return "play the game", mouse_button_state
        if go_upgrade.colliderect(mouse_form) and mouse_button_state == 1:
            mouse_button_state = 2
            return "upgrade", mouse_button_state
        if back_main_menu.colliderect(mouse_form) and mouse_button_state == 1:
            mouse_button_state = 2
            return "sure quit 2", mouse_button_state
        else:
            return "map", mouse_button_state

    def upgrade(self, context: PygameContext, mouse_form, mouse_button_state, options_save: OptionsSave, ship):
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
        if self.mas_gun == 1:
            mas_gun_upgrade_button = context.screen.blit(self.upgrade_picture, (context.width / 4 - 100, context.height / 4 * 3 + 25))
            context.screen.blit(self.coin_picture, (context.width / 4 - 60, context.height / 4 * 3 + 55))
            print_text("200", 45, (255, 255, 255), (context.width / 4 + 20, context.height / 4 * 3 + 80), context)
        if self.mas_gun == 2:
            if self.hmmu >= 2:
                mas_gun_upgrade_button = context.screen.blit(self.upgrade_picture, (context.width / 4 - 100, context.height / 4 * 3 + 25))
                context.screen.blit(self.coin_picture, (context.width / 4 - 60, context.height / 4 * 3 + 55))
                print_text("500", 45, (255, 255, 255), (context.width / 4 + 20, context.height / 4 * 3 + 80), context)
            else:
                mas_gun_upgrade_button = context.screen.blit(self.upgrade_max_picture, (context.width / 4 - 100, context.height / 4 * 3 + 25))
                print_text("Max", 45, (255, 255, 255), (context.width / 4, context.height / 4 * 3 + 80), context)
        if self.mas_gun == 3:
            if self.hmmu >= 3:
                mas_gun_upgrade_button = context.screen.blit(self.upgrade_picture, (context.width / 4 - 100, context.height / 4 * 3 + 25))
                context.screen.blit(self.coin_picture, (context.width / 4 - 60, context.height / 4 * 3 + 55))
                print_text("1000", 45, (255, 255, 255), (context.width / 4 + 20, context.height / 4 * 3 + 80), context)
            else:
                mas_gun_upgrade_button = context.screen.blit(self.upgrade_max_picture, (context.width / 4 - 100, context.height / 4 * 3 + 25))
                print_text("Max", 45, (255, 255, 255), (context.width / 4, context.height / 4 * 3 + 80), context)
        if self.mas_gun == 4:
            mas_gun_upgrade_button = context.screen.blit(self.upgrade_max_picture, (context.width / 4 - 100, context.height / 4 * 3 + 25))
            print_text("Max", 45, (255, 255, 255), (context.width / 4, context.height / 4 * 3 + 80), context)

        if self.hmmu >= 2:
            print_text((options_save.languages[options_save.select_language])["ship shield"], 45, (255, 255, 255), (context.width / 4, context.height / 4 - 50), context)
            print_text((options_save.languages[options_save.select_language])["level"] + " " + str(self.ship_def), 45, (255, 255, 255), (context.width / 4, context.height / 4), context)
            if self.ship_def == 1:
                ship_def_upgrade_button = context.screen.blit(self.upgrade_picture, (context.width / 4 - 100, context.height / 4 + 25))
                context.screen.blit(self.upgrader_box_picture, (context.width / 4 - 60, context.height / 4 + 55))
                print_text("1", 45, (255, 255, 255), (context.width / 4 + 40, context.height / 4 + 80), context)
            if self.ship_def == 2:
                ship_def_upgrade_button = context.screen.blit(self.upgrade_max_picture, (context.width / 4 - 100, context.height / 4 + 25))
                print_text("Max", 45, (255, 255, 255), (context.width / 4, context.height / 4 + 80), context)

        if self.hmmu >= 3:
            print_text((options_save.languages[options_save.select_language])["bomb"], 45, (255, 255, 255), (context.width / 4 * 3 - 50, context.height / 4 - 50), context)
            print_text((options_save.languages[options_save.select_language])["level"] + " " + str(self.bomb), 45, (255, 255, 255), (context.width / 4 * 3 - 50, context.height / 4), context)
            if self.bomb == 0:
                bomb_upgrade_button = context.screen.blit(self.upgrade_picture, (context.width / 4 * 3 - 150, context.height / 4 + 25))
                context.screen.blit(self.upgrader_box_picture, (context.width / 4 * 3 - 110, context.height / 4 + 55))
                print_text("3", 45, (255, 255, 255), (context.width / 4 * 3 - 10, context.height / 4 + 80), context)
            else:
                bomb_upgrade_button = context.screen.blit(self.upgrade_max_picture, (context.width / 4 * 3 - 150, context.height / 4 + 25))
                print_text("Max", 45, (255, 255, 255), (context.width / 4 * 3 - 50, context.height / 4 + 80), context)

        if mas_gun_upgrade_button.colliderect(mouse_form) and mouse_button_state == 1:
            if self.mas_gun == 1 and self.coin >= 200:
                mouse_button_state = 2
                self.mas_gun = 2
                self.coin = self.coin - 200
            if self.mas_gun == 2 and self.coin >= 500 and self.hmmu >= 2:
                mouse_button_state = 2
                self.mas_gun = 3
                self.coin = self.coin - 500
            if self.mas_gun == 3 and self.coin >= 1000 and self.hmmu >= 3:
                mouse_button_state = 2
                self.mas_gun = 4
                self.coin = self.coin - 1000
            self.write_file()

        if self.hmmu >= 2:
            if ship_def_upgrade_button.colliderect(mouse_form) and mouse_button_state == 1 and self.upgrade_box >= 1 and self.ship_def == 1:
                mouse_button_state = 2
                self.ship_def = self.ship_def + 1
                self.upgrade_box = self.upgrade_box - 1
                self.write_file()

        if self.hmmu >= 3:
            if bomb_upgrade_button.colliderect(mouse_form) and mouse_button_state == 1 and self.upgrade_box >= 3 and self.bomb == 0:
                mouse_button_state = 2
                self.bomb = self.bomb + 1
                self.upgrade_box = self.upgrade_box - 3
                self.write_file()

        if back_main_menu.colliderect(mouse_form):
            context.screen.blit(self.button_plate_on, (context.width / 4 * 3 + 60, 590))
            print_text((options_save.languages[options_save.select_language])["back"], 45, (255, 255, 255), ((1280 / 4 * 3 + 180), 675), context)
        if go_map.colliderect(mouse_form):
            context.screen.blit(self.button_plate_on, (context.width / 4 * 3 + 60, 50))
            print_text((options_save.languages[options_save.select_language])["map"], 45, (255, 255, 255), ((1280 / 4 * 3 + 180), 135), context)

        if back_main_menu.colliderect(mouse_form) and mouse_button_state == 1:
            mouse_button_state = 2
            return "sure quit 3", mouse_button_state
        if go_map.colliderect(mouse_form) and mouse_button_state == 1:
            mouse_button_state = 2
            return "map", mouse_button_state
        else:
            return "upgrade", mouse_button_state
        
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
            
