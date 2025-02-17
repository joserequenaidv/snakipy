import pygame as pg
import os
from src.settings import *

class LazyLoader:
    def __init__(self):
        self.game_folder = os.path.dirname(os.path.dirname(__file__))
        self.img_folder = os.path.join(self.game_folder, SPRITE_FOLDER)
        self.cache = {}
    
    def get_image(self, filename):
        if filename in self.cache:
            return self.cache[filename]
        
        path = os.path.join(self.img_folder, filename)
        
        try:
            image = pg.image.load(path).convert_alpha()
            self.cache[filename] = image
            return image
        
        except pg.error as e:
            print(f"Could not load image {filename}: {e}")
            surface = pg.Surface((TILESIZE, TILESIZE))
            surface.fill(LIGHTGREY)
            return surface
            
 