#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Flappy
# Copyright (C) 2014 Alan Aguiar
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact information:
# Alan Aguiar alanjas@hotmail.com

gtk_present = True
try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
except (ImportError, ValueError):
    gtk_present = False

import pygame

from resources import loadSound, loadImage

from floor import Floor
from pipe import Pipe_I
from pipe import Pipe_S
from background import Background
from bird import Bird
from scores import EndScore
from scores import Message
from scores import CurrentScore

FLOOR_Y = 50
DIST = 160
PIPE_W = 91
MIN_PIPE_H = 40 + 42
MIN_HEIGHT = MIN_PIPE_H * 2 + DIST + FLOOR_Y
MES_W = 227
MES_H = 251
PIPE_IH = 122

INIT = 0
PLAY = 1
END = 2
PAUSE = 3

INIT_BIRD_SPEED = 8
FPS = 30

GAME_SIZE = (400, 900)
MIN_SIZE = (320, MIN_HEIGHT + 160)


class Flappy():

    def __init__(self):
        self.running = False
        self.state = INIT
        self.best_scores = [0, 0, 0]
        self.sound = True
        self.level = 3  # Default: 3 for hard
        self._factor = 1  # Default: 1 for hard
        self.game_w = GAME_SIZE[0]
        self.game_h = GAME_SIZE[1]

    def increment_score(self):
        self.score = self.score + 1
        self.currentS.set_score(self.score)
        if self.sound_enable and self.sound:
            self._snd_pipe.play()

    def load_all(self):
        self.hit_flag = False
        self.floor_y = self.game_h - FLOOR_Y
        self.bird_x = self.game_w / 3 - FLOOR_Y
        self.bird_y = self.game_h / 2
        self.pipe_w = PIPE_W
        self.build_y = self.floor_y - 229
        self.mes_x = (self.game_w - MES_W) / 2
        self.mes_y = (self.game_h - MES_H) / 2
        self.game_p = self.game_w - DIST - self.pipe_w
        self.max_s = self.floor_y - MIN_PIPE_H - DIST
        self.min_pipe_h = MIN_PIPE_H
        self.end_s_x = (self.game_w - 139) / 2
        self.sc_x = (self.game_w - 70) / 2
        self.score = 0
        self.sprites = pygame.sprite.LayeredUpdates()
        self.tubes = pygame.sprite.LayeredUpdates()
        #######################################################################
        # load once reused images
        self._pipe_head = loadImage('head_pipe.png')
        self._pipe_body = loadImage('pipe.png')
        self._back = loadImage('score_alfa.png')
        self._mes = loadImage('init_alfa.png')
        #######################################################################
        self.background = Background(self, self._factor)
        self.background.mVel = 0
        self.floor = Floor(0, self.floor_y, self.game_w)
        self.floor.mVel = 0
        self.bird = Bird(self, self._factor, self.bird_x, self.bird_y)
        self.end_scores = EndScore(self, self.end_s_x, 200)
        self.message = Message(self, self.mes_x, self.mes_y)
        self.currentS = CurrentScore(self, self.sc_x, 100)
        #######################################################################
        self.sprites.add(self.background, layer=-1)
        self.sprites.add(self.floor, layer=0)
        self.sprites.add(self.bird, layer=2)
        self.sprites.add(self.message, layer=3)

    def set_level(self, level):
        if level not in (1, 2, 3):
            raise ValueError("level must be 1, 2 or 3")
        if level == self.level:
            return
        self.level = level
        self._factor = self.level / 3.0
        if self.running:
            self.state = INIT
            self.load_all()

    def resize(self, size):
        # Sugar's configure event describes the whole activity, including its
        # toolbar. Use the actual canvas allocation after pumping GTK events.
        canvas = getattr(self, 'canvas', None)
        if canvas is not None:
            allocation = canvas.get_allocation()
            size = (allocation.width, allocation.height)
        if size[0] <= 0 or size[1] <= 0:
            return
        # Keep enough room for both pipes and the gap, even in a tiny window.
        size = (max(MIN_SIZE[0], size[0]), max(MIN_SIZE[1], size[1]))
        if (size == (self.game_w, self.game_h) and
                pygame.display.get_surface().get_size() == size):
            return
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        if canvas is not None:
            canvas._screen = self.screen  # Keep Sugar previews in sync.
        self.game_w, self.game_h = self.screen.get_size()
        self.state = INIT
        self.load_all()

    def load_game(self):
        pipe1 = Pipe_I(self, self.game_w, PIPE_IH, self._factor)
        pipe2 = Pipe_S(self, self.game_w, self.floor_y - PIPE_IH - DIST,
                       self._factor)
        self.sprites.add(pipe1, layer=1)
        self.sprites.add(pipe2, layer=1)
        self.tubes.add(pipe1)
        self.tubes.add(pipe2)
        self.tubes.add(self.floor)
        self.sprites.add(self.currentS, layer=3)
        self.background.mVel = 5 * self._factor
        self.floor.mVel = -5 * self._factor
        self.sprites.remove(self.end_scores)
        self.sprites.remove(self.message)

    def check_collision(self, sprite1, sprite2):
        if not sprite1.rect.colliderect(sprite2.rect):
            return False
        x_offset = sprite2.rect.x - sprite1.rect.x
        y_offset = sprite2.rect.y - sprite1.rect.y
        offset = (x_offset, y_offset)
        return sprite1.mask.overlap(sprite2.mask, offset) is not None

    def run(self):
        if self.running:
            return
        pygame.display.init()
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.get_surface()
        if self.screen:
            self.game_w, self.game_h = self.screen.get_size()
        else:
            self.screen = pygame.display.set_mode(GAME_SIZE, pygame.RESIZABLE)
            pygame.display.set_caption('Flappy')
        self.sound_enable = True
        try:
            pygame.mixer.init()
            self._snd_pipe = loadSound('pipe.ogg', 0.5)
            self._snd_bird = loadSound('bird.ogg', 0.5)
            self._snd_hit = loadSound('hit.ogg', 0.15)
        except (pygame.error, OSError):
            self.sound_enable = False
        # cargo todo
        self.load_all()
        self.state = INIT
        self.running = True
        while self.running:
            if gtk_present:
                while Gtk.events_pending():
                    Gtk.main_iteration()
            if not self.running:
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                elif event.type == pygame.VIDEORESIZE:
                    self.resize(event.size)
                elif event.type == pygame.MOUSEBUTTONDOWN or (
                    event.type == pygame.KEYDOWN and
                    event.key in (pygame.K_SPACE, pygame.K_UP)):
                    if self.state == INIT:
                        self.state = PLAY
                        self.load_game()
                    elif self.state == PLAY:
                        self.bird.mVel = INIT_BIRD_SPEED * self._factor ** 0.7
                        self.bird.counter = 0
                        if self.sound_enable and self.sound:
                            self._snd_bird.play()
                    elif self.state == END:
                        self.state = INIT
                        self.load_all()
                    elif self.state == PAUSE:
                        self.state = PLAY
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_p, pygame.K_ESCAPE]:
                        if self.state == PAUSE:
                            self.state = PLAY
                        elif self.state == PLAY:
                            self.state = PAUSE

            if not self.running:
                break
            if self.state == PAUSE:
                self.clock.tick(FPS)
                continue

            self.sprites.update()
            self.sprites.draw(self.screen)

            if self.state == PLAY and any(
                    self.check_collision(self.bird, sprite)
                    for sprite in self.tubes):
                if self.sound_enable and self.sound and not self.hit_flag:
                    self._snd_hit.play()
                    self.hit_flag = True
                self.state = END
                self.floor.mVel = 0
                self.background.mVel = 0
                for spr in self.tubes:
                    spr.mVel = 0
                if self.score > self.best_scores[self.level - 1]:
                    self.best_scores[self.level - 1] = self.score
                self.end_scores.update_scores(self.score,
                                              self.best_scores[self.level - 1])
                self.sprites.add(self.end_scores, layer=3)
                self.sprites.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    pygame.init()
    g = Flappy()
    try:
        g.run()
    finally:
        pygame.quit()

