#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from resources import loadFont
from gettext import gettext as _



WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (252, 120, 88)

OUTLINE_COLOR = BLACK
OUTLINE_THICKNESS = 3


def text_with_outline(font, text, fg_color, outline_color, thickness):
    fg_surface = font.render(text, True, fg_color)
    outline_surface = font.render(text, True, outline_color)

    width, height = fg_surface.get_size()
    outline_size = (width + 2 * thickness, height + 2 * thickness)
    result_surface = pygame.Surface(outline_size, pygame.SRCALPHA, 32)
    result_surface = result_surface.convert_alpha()

    for x_offset in range(-thickness, thickness + 1):
        for y_offset in range(-thickness, thickness + 1):
            result_surface.blit(outline_surface,
                                (thickness + x_offset, thickness + y_offset))

    result_surface.blit(fg_surface, (thickness, thickness))
    return result_surface


class EndScore(pygame.sprite.Sprite):

    def __init__(self, parent, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.mPos = [x, y]
        self.score = 0
        self.best = 0
        self.font15 = loadFont('minercraftory.regular.ttf', 15)
        self.font23 = loadFont('minercraftory.regular.ttf', 23)
        self.font25 = loadFont('minercraftory.regular.ttf', 25)
        self.fgColor = WHITE
        self.mes_color = ORANGE
        self.mes_score = _('Score')
        self.mes_best = _('Best')
        self.mes_button = _('Restart')
        self._update_image()

    def update_scores(self, score, best):
        self.score = score
        self.best = best
        self._update_image()

    def _update_image(self):
        self.image = self.parent._back.copy()
        w = self.image.get_width()
        # score
        fontSurface = self.font15.render(self.mes_score, True, self.mes_color)
        xPos = (w - fontSurface.get_width()) / 2
        self.image.blit(fontSurface, (xPos, 10))
        # score number
        fontSurface = text_with_outline(self.font25, str(self.score),
                                        self.fgColor, OUTLINE_COLOR,
                                        OUTLINE_THICKNESS)
        xPos = (w - fontSurface.get_width()) / 2
        self.image.blit(fontSurface, (xPos, 35))
        # best
        fontSurface = self.font15.render(self.mes_best, True, self.mes_color)
        xPos = (w - fontSurface.get_width()) / 2
        self.image.blit(fontSurface, (xPos, 80))
        # best number
        fontSurface = text_with_outline(self.font25, str(self.best),
                                        self.fgColor, OUTLINE_COLOR,
                                        OUTLINE_THICKNESS)
        xPos = (w - fontSurface.get_width()) / 2
        self.image.blit(fontSurface, (xPos, 97))
        # restart
        fontSurface = self.font23.render(self.mes_button, True, self.fgColor)
        xPos = (w - fontSurface.get_width()) / 2
        self.image.blit(fontSurface, (xPos, 185))
        # update rect
        self.rect = self.image.get_rect()
        self.rect.x = self.mPos[0]
        self.rect.y = self.mPos[1]


class CurrentScore(pygame.sprite.Sprite):

    def __init__(self, parent, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.mPos = [x, y]
        self.points = 0
        self.image = self.parent._back
        self.size = [50, 60]
        self.font = loadFont('minercraftory.regular.ttf', 40)
        self.fgColor = WHITE
        self.bgColor = (113, 197, 207)
        self._update_image()

    def set_score(self, x):
        self.points = x
        self._update_image()

    def _update_image(self):
        fontSurface = text_with_outline(
            self.font, str(self.points), self.fgColor,
            OUTLINE_COLOR, OUTLINE_THICKNESS)
        self.size[0] = fontSurface.get_width()
        self.image = pygame.Surface(self.size)
        self.image.fill(self.bgColor)
        self.image.set_colorkey(self.bgColor)
        self.image.blit(fontSurface, (0, 0))
        self.rect = self.image.get_rect()
        self.mPos[0] = (self.parent.game_w - self.size[0]) / 2
        self.rect.x = self.mPos[0]
        self.rect.y = self.mPos[1]


class Message(pygame.sprite.Sprite):

    def __init__(self, parent, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.mPos = [x, y]
        self.image = self.parent._mes
        self.rect = self.image.get_rect()
        self.rect.x = self.mPos[0]
        self.rect.y = self.mPos[1]
