import pygame as pg
import os
from src.settings import *

class LazyLoader:
    def __init__(self):
        self.game_folder = os.path.dirname(__file__)
        self.img_folder = os.path.join(self.game_folder, SPRITE_FOLDER)
        self.cache = {}
        
        
 