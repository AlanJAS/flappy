#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from resources import loadImage

class Floor(pygame.sprite.Sprite):

    def __init__(self, x=0, y=0, large=100):
        pygame.sprite.Sprite.__init__(self)
        self.mPos = [x, y]
        self.p = large // 66 + 2
        self.large = self.p * 66
        self.image = pygame.surface.Surface((self.large, 16), 0)
        piece = loadImage('floor.png')
        for i in range(self.p):
            self.image.blit(piece, (i * 66, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.mPos[0]
        self.rect.y = self.mPos[1]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.mPos[0] = self.mPos[0] + self.mVel
        if self.mPos[0] <= -65:
            self.mPos[0] = 0
        self.rect.x = self.mPos[0]
