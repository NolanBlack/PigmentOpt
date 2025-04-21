import pygame as pg
from pigmentopt.constants import *

class PaintBucket(pg.sprite.Sprite):

    def __init__(self, index, num_buckets, color, callback=None):
        pg.sprite.Sprite.__init__(self)
        self.index = index
        self.num_buckets = num_buckets
        self.color = color
        if callback is None:
            self.callback = self._placeholder
        else:
            self.callback = callback
        self.reset()


    def _update_bucket(self):
        self.image = pg.Surface((2*DIM_BUCKET_RAD, 2*DIM_BUCKET_RAD))
        self.image.fill(COLOR_PALETTE)
        pg.draw.circle(self.image, self.color,
                       (DIM_BUCKET_RAD, DIM_BUCKET_RAD),
                       (self.health - HEALTH_PER_CLICK)/100. * DIM_BUCKET_RAD)
        pos = (self.index*DELTA_BUCKET + DIM_SCREEN[0]/2. - self.num_buckets*DELTA_BUCKET/2 + DELTA_BUCKET/2,
               500)
        self.rect = self.image.get_rect(center=pos)
        if self.health > 0:
            self.health -= HEALTH_PER_CLICK
            return self.color, HEALTH_PER_CLICK
        else:
            return self.color, 0

    def reset(self):
        self.health = 100 + HEALTH_PER_CLICK
        self._update_bucket()


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
                    print(f'PaintBucket pressed. health = {self.health}')
                    self.callback()
                    return self._update_bucket()
        return self.color, 0


