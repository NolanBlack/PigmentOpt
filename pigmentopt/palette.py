import pygame as pg
from pigmentopt.constants import *

class Palette(pg.sprite.Sprite):

    def __init__(self, screen, dim=(DIM_PALETTE)):
        pg.sprite.Sprite.__init__(self)


        self.active = True
        self.pos = POS_PALETTE
        self.image = pg.Surface(DIM_PALETTE)
        self.image.fill(COLOR_PALETTE)
        self.rect = self.image.get_rect(topleft=self.pos)

    def draw(self, surface):
        surface.blit(self.image, self.pos)


