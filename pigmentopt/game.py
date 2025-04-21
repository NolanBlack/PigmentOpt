import pygame as pg
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pigmentopt.constants import *
from pigmentopt.paint_bucket import PaintBucket
from pigmentopt.palette import Palette
from pigmentopt.levels import Levels
from pigmentopt.button import Button 
from pigmentopt.window import WindowSummary, WindowConfirm, WindowMode, WindowPalette
from pigmentopt import mixbox


class Game:

    def __init__(self):
        self.screen = pg.display.set_mode(DIM_SCREEN)
        self.clock = pg.time.Clock()

        self.mode = MODE_LEVELED
        self.current_palettte = DEFAULT_PALETTE.copy()
        self.current_levels = DEFAULT_LEVELS.copy()
        self.done = False
        self.new_game()

    def new_game(self):
        self.x = 0
        self.click_count = 0
        self.update_buckets()
        self.button_quit = Button(self.screen, POS_BUTTON_QUIT, COLOR_BUTTON, "Quit", dim=DIM_BUTTON_BOX)
        self.button_new = Button(self.screen, POS_BUTTON_NEW, COLOR_BUTTON, "New Game", dim=DIM_BUTTON_BOX)
        self.button_mode = Button(self.screen, POS_BUTTON_MODE, COLOR_BUTTON, "Mode Select", dim=DIM_BUTTON_BOX)
        self.button_palette = Button(self.screen, POS_BUTTON_PALETTE, COLOR_BUTTON, "Change Palette", dim=DIM_BUTTON_BOX)
        self.button_reset = Button(self.screen, POS_BUTTON_RESET, COLOR_BUTTON, "Reset Palette", dim=DIM_BUTTON_BOX)
        self.button_next = Button(self.screen, POS_BUTTON_CHECK, COLOR_BUTTON, "Check -->", dim=DIM_BUTTON_BOX)
        self.palette = Palette(self.screen)
        self.levels = Levels(self.current_levels, self.screen, POS_BUTTON_LEVEL, dim=DIM_LEVEL_BOX)
        self.window_summary = WindowSummary(self.screen)
        self.window_confirm = WindowConfirm(self.screen)
        self.window_mode = WindowMode(self.screen, self.mode)
        self.window_palette = WindowPalette(self.screen, self.current_palettte)

    def reset(self):
        for bucket in self.buckets:
            bucket.reset()

    def next_level(self):
        if self.levels.level_idx == len(self.current_levels) - 1:
            if self.mode == MODE_LEVELED:
                self.levels.level_idx = 0
                print('hooray!')
                self.window_summary.is_active = True
                self.run_window(self.window_summary)
                self.new_game()
            elif self.mode == MODE_ZEN:
                # TODO add a random level generator
                self.current_levels.append(COLOR_CADMIUM_RED)
                self.levels.current_levels = self.current_levels
        else:
            self.reset()
            self.levels.next()

    def update_buckets(self):
        self.buckets = pg.sprite.Group(
            *[PaintBucket(i, len(self.current_palettte), c, callback=self.count_clicks) for i, c in enumerate(self.current_palettte)]
        )

    # A callback function that we pass to button instance
    def count_clicks(self):
        """Increase self.x if button is pressed."""
        self.click_count += 1

    def run(self):
        pg.init()
        while not self.done:
            self.handle_events()
            self.run_logic()
            self.draw()
            self.clock.tick(30)
        pg.quit()

    def run_window(self, window):
        while window.is_active:
            window.handle_events()
            self.draw()
            self.clock.tick(30)

    def handle_events(self):
        for event in pg.event.get():
            # quit
            if event.type == pg.QUIT:
                self.done = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.done = True

            # buttons and menus
            if self.button_new.handle_event(event):
                self.window_confirm.is_active = True
                self.run_window(self.window_confirm)
                if self.window_confirm.is_yes:
                    self.new_game()
            elif self.button_quit.handle_event(event):
                self.window_confirm.is_active = True
                self.run_window(self.window_confirm)
                if self.window_confirm.is_yes:
                    self.done = True
                print("Quit Clicked")
            elif self.button_next.handle_event(event):
                self.next_level()
                print("Next Clicked")
            elif self.button_reset.handle_event(event):
                self.reset()
                print("Reset Clicked")
            elif self.button_mode.handle_event(event):
                self.window_mode.is_active = True
                self.run_window(self.window_mode)
                self.mode = self.window_mode.mode
                print("Mode Clicked")
                self.new_game()
            elif self.button_palette.handle_event(event):
                self.window_palette.is_active = True
                self.run_window(self.window_palette)
                self.current_palettte = self.window_palette.current_palette
                self.update_buckets()
                self.reset()
                print("Palette Clicked")

            # add paint
            for bucket in self.buckets:
                c, h = bucket.handle_event(event)
                self.x += h


    def draw(self):
        # render BG
        self.screen.fill(COLOR_BG )

        # render sprites
        self.palette.draw(self.screen)
        self.buckets.draw(self.screen)
        self.button_quit.draw(self.screen)
        self.button_new.draw(self.screen)
        self.button_mode.draw(self.screen)
        self.button_palette.draw(self.screen)
        self.button_reset.draw(self.screen)
        self.button_next.draw(self.screen)
        self.levels.draw(self.screen)
        self.window_summary.draw(self.screen)
        self.window_confirm.draw(self.screen)
        self.window_mode.draw(self.screen)
        self.window_palette.draw(self.screen)

        # render fonts
        txt = FONT.render(f"x = {self.x}", True, COLOR_FONT)
        self.screen.blit(txt, POS_DEBUG)

        # TODO
        # display:
        #  - mode
        #  - title
        #  - score

        pg.display.flip()


    def run_logic(self):
        self.buckets.update()
