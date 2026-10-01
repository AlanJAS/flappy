#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from resources import loadImage

SKY = (113, 197, 207)
GROUND = (221, 216, 148)


class Background(pygame.sprite.Sprite):

    def __init__(self, parent, factor):
        pygame.sprite.Sprite.__init__(self)
        self.pos_x = 0

        bg_image = loadImage('buildings.png')
        self.bg_width = bg_image.get_width()

        # scale_factor for bg to match window
        scale_factor = int(
            parent.game_w / self.bg_width) + 2

        self.image = pygame.surface.Surface((self.bg_width * scale_factor,
                                            parent.game_h))

        # Add sky and ground
        self.image.fill(SKY)
        rect = pygame.rect.Rect(0, parent.floor_y,
                                self.bg_width * scale_factor,
                                parent.game_h - parent.floor_y)
        self.image.fill(GROUND, rect)

        # Add buildings
        for i in range(scale_factor):
            self.image.blit(bg_image, (self.bg_width * i,
                                       parent.floor_y - 229))

        self.rect = self.image.get_rect()
        self.rect.x = self.pos_x

    def update(self):
        self.pos_x -= self.mVel
        if self.pos_x <= -(self.bg_width):
            self.pos_x = 0
        self.rect.x = round(self.pos_x)
