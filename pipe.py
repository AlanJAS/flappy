#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import random

class Pipe_I(pygame.sprite.Sprite):

    def __init__(self, parent, x, height, factor):
        pygame.sprite.Sprite.__init__(self)
        self.flag = True
        self.points = True
        self.parent = parent
        self.mPos = [x, 500]
        self.factor = factor
        self.mVel = -5 * self.factor
        h = height - 42
        self.p = h // 40
        self.height = self.p * 40 + 50
        self.mPos[1] = self.parent.floor_y - self.height
        self.image = pygame.surface.Surface((91, self.height), 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.image.fill((255, 255, 255))
        self.image.blit(self.parent._pipe_head, (0, 0))
        for i in range(self.p):
            self.image.blit(self.parent._pipe_body, (4, 42 + i * 40))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = self.mPos[0]
        self.rect.y = self.mPos[1]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.mPos[0] = self.mPos[0] + self.mVel
        self.rect.x = self.mPos[0]
        self.rect.y = self.mPos[1]

        if self.mPos[0] < -91:
            self.parent.sprites.remove(self)
            self.parent.tubes.remove(self)

        elif self.mPos[0] < (self.parent.bird_x - self.parent.pipe_w / 2):
            if self.points:
                self.points = False
                self.parent.increment_score()

        elif self.mPos[0] < (self.parent.game_p):
            if self.flag:
                self.flag = False

                mi = self.height - 160
                ma = self.height + 160
                if mi < 82:
                    mi = 82
                if ma > self.parent.max_s:
                    ma = self.parent.max_s

                h = random.randrange(mi, ma)
                p = Pipe_I(self.parent, self.parent.game_w, h, self.factor)
                self.parent.sprites.add(p, layer=1)
                self.parent.tubes.add(p)
                s = self.parent.floor_y - p.height - 160
                p = Pipe_S(self.parent, self.parent.game_w, s, self.factor)
                self.parent.sprites.add(p, layer=1)
                self.parent.tubes.add(p)


class Pipe_S(pygame.sprite.Sprite):

    def __init__(self, parent, x, height, factor):
        pygame.sprite.Sprite.__init__(self)
        self.flag = True
        self.parent = parent
        self.mPos = [x, 0]
        self.mVel = -5 * factor
        h = height - 42
        self.p = h // 40
        self.height = self.p * 40 + 42
        if self.height > height:
            dx = self.height - height
            self.mPos[1] = -dx
        self.image = pygame.surface.Surface((91, self.height), 0)
        self.image.fill((255, 255, 255))

        for i in range(self.p):
            self.image.blit(self.parent._pipe_body, (4, i * 40))
        self.image.blit(self.parent._pipe_head, (0, self.p * 40))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = self.mPos[0]
        self.rect.y = self.mPos[1]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.mPos[0] = self.mPos[0] + self.mVel
        self.rect.x = self.mPos[0]

        if self.mPos[0] < -91:
            self.parent.sprites.remove(self)
            self.parent.tubes.remove(self)
