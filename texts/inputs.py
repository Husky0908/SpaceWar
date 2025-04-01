import pygame
from base.context import PygameContext
from texts.text_print import print_text


class TextInput:
    def __init__(self):
        self.abc_dict = {pygame.K_BACKSPACE: "backspace",
                         pygame.K_ESCAPE: "escape",
                         pygame.K_SPACE: " ",
                         pygame.K_0: "0",
                         pygame.K_1: "1",
                         pygame.K_2: "2",
                         pygame.K_3: "3",
                         pygame.K_4: "4",
                         pygame.K_5: "5",
                         pygame.K_6: "6",
                         pygame.K_7: "7",
                         pygame.K_8: "8",
                         pygame.K_9: "9",
                         pygame.K_a: "a", pygame.K_b: "b", pygame.K_c: "c", pygame.K_d: "d", pygame.K_e: "e",
                         pygame.K_f: "f", pygame.K_g: "g", pygame.K_h: "h", pygame.K_i: "i", pygame.K_j: "j",
                         pygame.K_k: "k", pygame.K_l: "l", pygame.K_m: "m", pygame.K_n: "n", pygame.K_o: "o",
                         pygame.K_p: "p", pygame.K_q: "q", pygame.K_r: "r", pygame.K_s: "s", pygame.K_t: "t",
                         pygame.K_u: "u", pygame.K_v: "v", pygame.K_w: "w", pygame.K_x: "x", pygame.K_y: "y",
                         pygame.K_z: "z",
                         pygame.K_UP: "up arrow",
                         pygame.K_DOWN: "down arrow",
                         pygame.K_RIGHT: "right arrow",
                         pygame.K_LEFT: "left arrow"}
        self.word_list = []
        self.word_time = 0
        self.word = ""


    def input_player(self, context: PygameContext):
        input_run = True
        while input_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    input_run = False

            for i in self.abc_dict.keys():
                keys = pygame.key.get_pressed()
                if context.time - self.word_time >= 100:
                    if keys[i] and not self.abc_dict[i] == "backspace":
                        self.word_list.append(self.abc_dict[i])
                        self.word_time = context.time
                    if keys[i] and self.abc_dict[i] == "backspace":
                        self.word_list = []
                        #word_list_2 = []
                        #for b in range(len(self.word_list) - 1):
                        #    word_list_2.append(self.word_list[b - 1])
                        #self.word_list = word_list_2
            self.word = ""
            for i in range(len(self.word_list)):
                self.word = self.word + self.word_list[i - 1]
            print(self.word)
            print_text(self.word, 50, (255, 255, 255), (300, 300), context)
            context.time = context.time + 1


            context.screen.fill((0, 0, 0))
            pygame.display.flip()