"""Locate bundled assets independently of the working directory"""

import os
import pygame

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMAGES_DIR = os.path.join(DATA_DIR, "images")
SOUNDS_DIR = os.path.join(DATA_DIR, "sounds")



def loadImage(name):
    """load an image, convert to screen format"""
    path = os.path.join(IMAGES_DIR, name)
    if not os.path.exists(path):
        return None
    image = pygame.image.load(path)
    if image.get_masks()[3]:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image

def loadSound(name, volume=0.5):
    """load a sound and set defined volume"""
    path = os.path.join(SOUNDS_DIR, name)
    if not os.path.exists(path):
        print('aca none', path)
        return None
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    return sound

def loadFont(name, size):
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        return None
    font = pygame.font.Font(path, size)
    return font
