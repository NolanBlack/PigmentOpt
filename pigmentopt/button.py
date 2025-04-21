import pygame as pg
from pigmentopt.constants import *

class Button(pg.sprite.Sprite):

    def __init__(self, screen, pos, color, text, dim=(DIM_BUTTON_BOX), font=FONT, font_color=COLOR_FONT):
        pg.sprite.Sprite.__init__(self)


        self.active = True
        self.text = text
        self.pos = pos
        self.image = pg.Surface(dim)
        self.font = font
        self.font_color = font_color
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, surface):
        if self.active:
            surface.blit(self.image, self.pos)
            surface.blit(self.font.render(self.text, True, self.font_color), (self.pos[0]+4, self.pos[1]+8))

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


