#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from resources import loadImage


class Bird(pygame.sprite.Sprite):

    def __init__(self, parent, factor, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.factor = factor
        self.parent = parent
        self.mVel = 0
        self.velocity_limit = -20 * self.factor ** 1.7
        self.acceleration = self.factor ** 0.6
        self.images = []
        self.index = 0
        self.counter = 0
        self.count_flap = 0
        for num in range(3):
            img = loadImage(f"bird_{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.y = float(self.rect.centery)
        self.mask = pygame.mask.from_surface(self.image)

    # handle the animation
    def wing_flap(self):
        self.flap_cooldown = 5
        self.count_flap += 1

        if self.count_flap > self.flap_cooldown:
            self.count_flap = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]

    def update(self):
        if self.parent.state in (0, 1):
            self.wing_flap()
        if self.parent.state != 0:
            # handle velocity
            self.counter += 1
            if self.counter > 5:
                self.mVel -= self.acceleration
            self.mVel = max(self.mVel, self.velocity_limit)
            self.y -= self.mVel

            if self.parent.state == 2:
                angle = -90
            else:
                angle = self.mVel * 2 / self.factor
            self.image = pygame.transform.rotate(self.images[self.index], angle)
            # Rotation changes the surface dimensions. Keep its center and rebuild
            # both the rect and mask from the same image used for drawing.
            self.rect = self.image.get_rect(center=(self.rect.centerx, round(self.y)))
            if self.rect.top < 0:
                self.rect.top = 0
                self.y = float(self.rect.centery)
            if self.parent.state == 2 and self.rect.bottom >= self.parent.floor_y:
                self.rect.bottom = self.parent.floor_y
                self.y = float(self.rect.centery)
                self.mVel = 0
            self.mask = pygame.mask.from_surface(self.image)

