import pygame as pg
from pigmentopt.constants import *

class Levels(pg.sprite.Sprite):

    def __init__(self, levels, screen, pos, dim=(DIM_LEVEL_BOX)):
        pg.sprite.Sprite.__init__(self)


        self.level_idx = 0
        self.current_levels = levels
        self.text = f"Level {self.level_idx+1}"
        self.pos = pos
        self.image = pg.Surface(dim)
        self.image.fill(self.current_levels[self.level_idx])
        self.rect = self.image.get_rect(topleft=pos)

    def next(self):
        self.level_idx += 1
        self.text = f"Level {self.level_idx+1}"
        self.image.fill(self.current_levels[self.level_idx])

    def draw(self, surface):
        surface.blit(self.image, self.pos)
        surface.blit(FONT.render(self.text, True, COLOR_FONT), (self.pos[0]+200, self.pos[1]-20))

    def handle_event(self, event):
        """Handle events that get passed from the event loop."""
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    # do something on click
                    pass
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True
        return False


