import pygame as pg
from pigmentopt.constants import *
from pigmentopt.button import Button 

class Window(pg.sprite.Sprite):

    def __init__(self, screen, dim=(DIM_PALETTE)):
        pg.sprite.Sprite.__init__(self)


        self.is_active = False
        self.pos = POS_WINDOW
        self.image = pg.Surface(DIM_WINDOW)
        self.image.fill(COLOR_WINDOW)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.buttons = []
        self.text_pos = (0,0)
        self.text = ""
        self.minitext_pos = (0,0)
        self.minitext = ""

    def _check_if_escaped(self, event):
        # quit
        if event.type == pg.QUIT:
            self.is_active = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.is_active = False

    def draw(self, surface):
        if self.is_active:
            surface.blit(self.image, self.pos)
            surface.blit(FONT.render(self.text, True, COLOR_FONT), (self.pos[0]+self.text_pos[0], self.pos[1]+self.text_pos[1]))
            surface.blit(MINIFONT.render(self.minitext, True, COLOR_FONT), (self.pos[0]+self.minitext_pos[0], self.pos[1]+self.minitext_pos[1]))
            for button in self.buttons:
                button.draw(surface)

class WindowSummary(Window):
    def __init__(self, screen, dim=(DIM_PALETTE)):
        super().__init__(screen, dim)
        self.button_ok = Button(screen, (DIM_SCREEN[0]/2 - 80,DIM_WINDOW[1]+100), COLOR_WINDOW, "        OK", dim=DIM_BUTTON_BOX)
        self.buttons.append(self.button_ok)
        self.text = "Final Score: TODO"
        self.text_pos = (DIM_WINDOW[0]/2 - 80 ,DIM_WINDOW[1]/2.5)

    def handle_events(self):
        #super().handle_events()
        for event in pg.event.get():
            self._check_if_escaped(event)
            if self.button_ok.handle_event(event):
                self.is_active = False


class WindowConfirm(Window):
    def __init__(self, screen, dim=(DIM_PALETTE)):
        super().__init__(screen, dim)
        self.button_no = Button(screen, (self.pos[0]+50, self.pos[1]+DIM_WINDOW[1]-80), COLOR_WINDOW, "        no", dim=DIM_BUTTON_BOX)
        self.button_yes = Button(screen, (self.pos[0]+DIM_WINDOW[0]-DIM_BUTTON_BOX[0] - 50, self.pos[1]+DIM_WINDOW[1]-80), COLOR_WINDOW, "        Yes", dim=DIM_BUTTON_BOX)
        self.buttons.append(self.button_no)
        self.buttons.append(self.button_yes)
        self.is_yes = False
        self.text = "are you sure?"
        self.text_pos = (DIM_WINDOW[0]/2 - 80 ,DIM_WINDOW[1]/2.5)


    def handle_events(self):
        #super().handle_events()
        for event in pg.event.get():
            self._check_if_escaped(event)
            if self.button_yes.handle_event(event):
                self.is_active = False
                self.is_yes = True
            if self.button_no.handle_event(event):
                self.is_active = False


class WindowPalette(Window):
    def __init__(self, screen, current_palette, dim=(DIM_PALETTE)):
        super().__init__(screen, dim)
        self.text = "Palette Selection"
        self.text_pos = (DIM_WINDOW[0]/2 - 80 ,20)
        self.button_clear = Button(screen, (self.pos[0]+40, self.pos[1]+DIM_WINDOW[1]-50), COLOR_WINDOW, "Clear Selection", dim=DIM_BUTTON_BOX)
        self.button_default = Button(screen, (self.pos[0] + 220,self.pos[1]+DIM_WINDOW[1]-50), COLOR_WINDOW, "    Default", dim=DIM_BUTTON_BOX)
        self.button_confirm = Button(screen, (self.pos[0]+370, self.pos[1]+DIM_WINDOW[1]-50), COLOR_WINDOW, "  Confirm", dim=DIM_BUTTON_BOX)
        self.buttons.append(self.button_clear)
        self.buttons.append(self.button_default)
        self.buttons.append(self.button_confirm)
        self.current_palette = current_palette
        self.update_display_text()

        self.mini_buttons = {}
        bx = 150
        by = 20

        col1 = len(COLOR_DICT) // 2
        entries_per_column = 5
        row_idx = 0
        for i, (key, value) in enumerate(COLOR_DICT.items()):
            if i % entries_per_column == 0:
                row_idx = 0
            col_idx = i // entries_per_column
            button = Button(screen, (self.pos[0]+40 + (bx+10)*col_idx, self.pos[1]+120+(by+5)*row_idx),
                            value, key,
                            dim = (bx, by),
                            font=MINIFONT,
                            font_color = tuple(255 - x for x in value)
                            )
            self.mini_buttons[key] = button
            self.buttons.append(button)
            row_idx += 1

    def handle_events(self):
        #super().handle_events()
        self.update_display_text()
        for event in pg.event.get():
            self._check_if_escaped(event)
            if self.button_default.handle_event(event):
                self.current_palette = DEFAULT_PALETTE.copy()
                self.update_display_text()
            if self.button_clear.handle_event(event):
                self.current_palette = []
                self.update_display_text()
            if self.button_confirm.handle_event(event):
                if len(self.current_palette) == 0:
                    self.current_palette = DEFAULT_PALETTE.copy()
                self.is_active = False

            for key, button in self.mini_buttons.items():
                if button.handle_event(event):
                    self.add_to_palette(key)

    def update_display_text(self):
        names = []
        for rgb in self.current_palette:
            for key,value in COLOR_DICT.items():
                if value == rgb:
                    names.append(key)
        self.minitext_pos = (20,100)

        self.minitext = " | ".join(names)


    def add_to_palette(self, key):
        if len(self.current_palette) >= MAX_PALETTE_LENGTH:
            print("Palette Full")
            return
        elif COLOR_DICT[key] in self.current_palette:
            return
        else:
            print("adding key")
            self.current_palette.append(COLOR_DICT[key])
        self.update_display_text()


class WindowMode(Window):
    def __init__(self, screen, mode, dim=(DIM_PALETTE)):
        super().__init__(screen, dim)
        self.text = "Mode Selection"
        self.text_pos = (DIM_WINDOW[0]/2 - 70 ,20)
        self.button_levels = Button(screen, (DIM_WINDOW[0]/2 + 70, DIM_WINDOW[1]-40), COLOR_WINDOW, "       Levels", dim=DIM_BUTTON_BOX)
        self.button_zen = Button(screen, (DIM_WINDOW[0]/2 + 70, DIM_WINDOW[1]+20), COLOR_WINDOW, "         Zen", dim=DIM_BUTTON_BOX)
        self.buttons.append(self.button_levels)
        self.buttons.append(self.button_zen)
        self.mode = mode

    def handle_events(self):
        #super().handle_events()
        for event in pg.event.get():
            self._check_if_escaped(event)
            if self.button_levels.handle_event(event):
                self.mode = MODE_LEVELED
                self.is_active = False
            if self.button_zen.handle_event(event):
                self.mode = MODE_ZEN
                self.is_active = False
