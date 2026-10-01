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
        if self.parent.state == 0 or self.parent.state == 1:
            self.wing_flap()
        if self.parent.state != 0:
            # handle velocity
            self.counter += 1
            if self.counter > 5:
                self.mVel -= self.acceleration
            if self.mVel < self.velocity_limit:
                self.mVel = self.velocity_limit

            # prevents bird from falling through floor after collision
            if self.rect.bottom > self.parent.floor_y:
                self.rect.y += int(self.mVel)

            # handle rotation
            self.image = pygame.transform.rotate(
                self.images[self.index], self.mVel * 2 / self.factor)
            self.mask = pygame.mask.from_surface(self.image)

            # handle bird y position
            self.rect.y -= int(self.mVel)
            if self.rect.y < 0:
                self.rect.y = 0

            # rotates bird after collision
            if self.parent.state == 2:
                self.image = pygame.transform.rotate(
                    self.images[self.index], -90)
